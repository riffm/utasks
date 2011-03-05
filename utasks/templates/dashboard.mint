#base: base.mint

#def body():
    @h1 utasks

    @h4 список задач

    #for issue in issues:
        @div.class(issue)
            @p.class(title) 
                @a.href({{ env.url_for('project', proj=issue.proj.id) }}) {{ issue.proj.name }}
                /
                @a.href({{ env.url_for('issue', issue=issue.id) }}) {{ issue.title }}

