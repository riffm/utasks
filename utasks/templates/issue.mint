#base: base.mint

#def body():
    @a.href({{ env.url_for('project', proj=issue.proj.id) }}) {{ issue.proj.name }}
    @h1 {{ issue.title }}
    @p автор: {{ issue.author.name }}
    @p исполнитель: {{ issue.executor.name }}
    #for comment in issue.comments:
        @p {{ comment.html }}
