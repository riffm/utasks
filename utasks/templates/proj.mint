#base: base.mint

#def body():
    @h1 {{ project.name }}
        #if env.user in project.users:
            @a.href({{ env.url_for('update-project', proj=project.id) }}) редактировать
    #if project.description:
        @p.class(description) {{ project.description }}

    @a.href({{ env.url_for('create-issue', proj=project.id) }}) создать задачу

    @h4 список задач

    #for issue in project.issues:
        @div.class(issue)
            @p.class(title) @a.href({{ env.url_for('issue', issue=issue.id) }}) {{ issue.title }}
