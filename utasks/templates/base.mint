{{ utils.doctype.html_transitional }}

#def media():


@html
    @head
        #media()
    @body
        #if 'user' in env and env.user:
            @p {{ env.user.name }} / {{ env.user.email }}
            @a.href({{ env.url_for('logout') }}) выйти
        #else:
            @a.href({{ env.url_for('login') }}) войти
        #body()

