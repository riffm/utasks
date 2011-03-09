#base: base.mint

#def body():
    #if form:
        @form.action({{ env.url_for('user', user_id=user.id) }}).method(POST)
            {{ form.render() }}
            @input.type(submit).value(Обновить данные о себе)
    #else:
        @h1 {{ user.name }} / {{ user.login }}
        @p {{ user.email }}

        #for project in user.projects:
            @div @a.href({{ env.url_for('project', proj=project.id) }}) {{ project.name }}

    #for issue in issues:
        @div @a.href({{ env.url_for('issue', issue=issue.id) }}) {{ issue.title }}
