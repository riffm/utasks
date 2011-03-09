#base: base.mint

#def body():
    @div @a.href({{ env.url_for('project', proj=issue.proj.id) }}) {{ issue.proj.name }}

    #if issue.author.id != issue.executor.id:
        @p
            Некто {{ issue.author.name }} хочет попросить
            {{ u'вас' if issue.executor.id == env.user.id else issue.executor.name }}
    #else:
        @p Вы хотите от себя следующее

    @h1 {{ issue.title }}

    #for comment, l in utils.loop(issue.comments):
        #if not l.first:
            @p @i {{ comment.author.name }}
        @p {{ comment.html }}

    #if env.user:
        @form.action({{ env.url_for('issue', issue=issue.id) }}).method(POST)
            {{ form.render() }}
            @input.type(submit).value(Комментировать)
