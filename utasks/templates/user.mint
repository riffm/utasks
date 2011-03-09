#base: base.mint

#def body():
    @h1 {{ user.name }} / {{ user.login }}
    @p {{ user.email }}

    #for project in user.projects:
        @div @a.href({{ env.url_for('project', proj=project.id) }}) {{ project.name }}

    #for issue in issues:
        @div @a.href({{ env.url_for('issue', issue=issue.id) }}) {{ issue.title }}
