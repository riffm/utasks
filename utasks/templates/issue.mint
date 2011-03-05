#base: base.mint

#def body():
    @a.href({{ env.url_for('project', proj=issue.proj.id) }}) {{ issue.proj.name }}
    @h1 {{ issue.title }}
    #for comment in issue.comments:
        @p {{ comment.html }}
