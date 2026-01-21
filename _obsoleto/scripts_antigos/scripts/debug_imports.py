modules = [
    'views.login_view',
    'views.main_view',
    'views.dashboard_view',
    'views.clientes_view',
    'views.emprestimos_view',
    'views.notificacoes_view'
]

for m in modules:
    try:
        print('Importing', m)
        __import__(m)
        print('OK', m)
    except Exception as e:
        import traceback
        print('ERROR importing', m)
        traceback.print_exc()
        break
