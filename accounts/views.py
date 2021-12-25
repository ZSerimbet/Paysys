import uuid
from decimal import Decimal

from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .manager import AccountManager
from transactions.manager import TransactionManager

def account_create_view(request):
    """
    Создание аккаунта.
    """

    # Инициализируем менеджер
    account_manager = AccountManager()

    # Если пришел POST-запрос
    if request.method == 'POST':
        # Создаем новый счёт
        account_manager.create({
            'currency': request.POST.get('currency', 'KZT'),
            'uuid': uuid.uuid4(),
            'balance': 0
        })

        # Обновляем страницу
        return redirect('/')
    else:
        # Если запрос был не POST, возвращаем HTTP статус 403
        return HttpResponseForbidden()


def accounts_erase_view(request):
    """
    Удаление всех счетов.
    """

    # Инициализируем менеджер
    account_manager = AccountManager()

    # Если пришел POST-запрос
    if request.method == 'POST':
        # Очищаем таблицу
        account_manager.erase()

        # Обновляем страницу
        return redirect('/')
    else:
        # Если запрос был не POST, возвращаем HTTP статус 403
        return HttpResponseForbidden()


def account_detail_view(request, uuid):
    """
    Подробная информация о счёте, транзакциях.
    """

    # Инициализируем менеджер
    account_manager = AccountManager()

    # Инициализируем менеджер
    transaction_manager = TransactionManager()

    # Получаем информацию о текущем счете
    account = account_manager.get(uuid)

    # Если такого счёта нет, редиректим на домашнюю страницу
    if not account:
        return redirect('/')

    # Получаем транзакции для текущего счёта
    transactions = transaction_manager.get(uuid)

    # Словарь хранящий данные которые передаются в HTML-шаблон
    context = {
        'account': account[0],
        'transactions': transactions
    }

    # Рендерим страницу
    return render(request, 'account_detail.html', context)


def account_refill_view(request, uuid):
    """
    Пополнение счёта.
    """

    # Инициализируем менеджер
    account_manager = AccountManager()

    # Инициализируем менеджер
    transaction_manager = TransactionManager()

    # Если пришел POST-запрос
    if request.method == 'POST':
        # Получаем данные из формы
        amount = request.POST.get('amount', 0)
        # Получаем данные из формы
        currency = request.POST.get('currency', '')

        # Пополняем счёт
        account_manager.refill({
            'balance': Decimal(amount),
            'uuid': uuid
        })

        # Создаём транзакцию о пополнении счёта
        transaction_manager.create({
            'type': 'refill',
            'currency': currency,
            'amount': Decimal(amount),
            'uuid': uuid
        })

        # Редиректим на предыдущую страницу
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        # Если запрос был не POST, возвращаем HTTP статус 403
        return HttpResponseForbidden()


def account_transfer_view(request, uuid):
    """
    Перевод со счёта на счёт
    """

    # Инициализируем менеджер
    account_manager = AccountManager()

    # Инициализируем менеджер
    transaction_manager = TransactionManager()

    # Если пришел POST-запрос
    if request.method == 'POST':
        # Получаем данные из формы
        amount = request.POST.get('amount', 0)
        # Получаем данные из формы
        currency = request.POST.get('currency', '')
        # Получаем данные из формы
        account = request.POST.get('account', '')

        # Получаем информацию о получателе из базы
        recipient = account_manager.get(account)
        # Получаем информацию о отправителе из базы
        sender = account_manager.get(uuid)

        # Если такой получатель есть
        # И если валюта кошельков совпадает
        # И если сумма отправления не больше доступной на счету
        # И если счёт получателя отличается от отправителя
        if recipient \
        and recipient[0][1] == currency \
        and int(amount) <= sender[0][3] \
        and account != uuid:
            # Списываем сумму со счета отправителя
            account_manager.writeoff({
                'balance': Decimal(amount),
                'uuid': uuid
            })

            # Создаём запись о транзакции списания со счёта отправителя
            transaction_manager.create({
                'type': 'writeoff',
                'currency': currency,
                'amount': Decimal(amount),
                'uuid': uuid
            })

            # Пополняем счёт получателя
            account_manager.refill({
                'balance': Decimal(amount),
                'uuid': account
            })

            # Создаём запись о транзакции пополнения счёта получателя
            transaction_manager.create({
                'type': 'refill',
                'currency': currency,
                'amount': Decimal(amount),
                'uuid': account
            })

        # Редиректим на предыдущую страницу
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        # Если запрос был не POST, возвращаем HTTP статус 403
        return HttpResponseForbidden()


def accounts_list_view(request):
    """
    Список счетов.
    """

    # Инициализируем менеджер
    account_manager = AccountManager()

    # Получаем список всех счетов из базы
    accounts = account_manager.all()

    # Тут мы сортируем список счетов, чтобы найти какой из них
    # нам выделить, как самый большой баланс для определенной валюты

    # Переменные которые будут хранить идентификатор записи в базе, 
    # когда мы найдем нужный нам идентификатор для каждой валюты,
    # каждая из этих переменных будет содержать идентификатор
    # с которым мы будем сравнивать потом в шаблоне
    max_kzt_id = max_usd_id = max_eur_id = 0;

    # Переменные хранящие максимальное значение баланса,
    # для каждой из валют, нужно только для сортировки
    max_kzt = max_usd = max_eur = 0;

    # Проходим по каждому счёту
    for account in accounts:
        # Если валюта "KZT", значит пытаемся найти кошелек с самым большим балансом
        if account[1] == "KZT":
            # Если баланс счёта больше чем результат предыдущей итерации
            # То перезаписываем максимальную найденную сумму, и идентификатор счёта этой суммы
            if account[3] > max_kzt:
                max_kzt = account[3]
                max_kzt_id = account[0]

        if account[1] == "USD":
            if account[3] > max_usd:
                max_usd = account[3]
                max_usd_id = account[0]

        if account[1] == "EUR":
            if account[3] > max_eur:
                max_eur = account[3]
                max_eur_id = account[0]

    # Словарь хранящий данные которые передаются в HTML-шаблон
    context = {
        'accounts': accounts,
        'max_kzt_id': max_kzt_id,
        'max_usd_id': max_usd_id,
        'max_eur_id': max_eur_id
    }

    # Рендерим страницу
    return render(request, 'accounts_list.html', context)