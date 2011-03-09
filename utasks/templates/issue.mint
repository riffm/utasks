#base: base.mint

#def body():
    @div @a.href({{ env.url_for('project', proj=issue.proj.id) }}) {{ issue.proj.name }}

    @p Данная задача — {{ u'закрыта' if issue.done else u'открыта' }}.

    @p
        #if issue.author.id != issue.executor.id:
            Некто {{ issue.author.name }} хочет попросить
            {{ u'вас' if env.user and issue.executor.id == env.user.id else issue.executor.name }}
        #elif env.user and issue.author.id == env.user.id:
            Данную задачу, Вы назначили себе сами.
        #else:
            Данную задачу, назначил себе {{ issue.author.name }}.

        #if issue.deadline:
            Срок — {{ issue.deadline.strftime('%d/%m/%Y') }}
        #else:
            Сроков нет.

    @h1 {{ issue.title }}

    #for comment, l in utils.loop(issue.comments):
        #if not l.first:
            @p @a.href({{ env.url_for('user', user_id=comment.author.id) }}) @i {{ comment.author.name }}
        @p {{ comment.html }}

    #if env.user:
        @form.action({{ env.url_for('issue', issue=issue.id) }}).method(POST)
            {{ form.render() }}
            @input.type(submit).value(Комментировать)
            #if env.user.id in (issue.author.id, issue.executor.id) and not issue.done:
                @button.name(comment_and_close).value(1) Комментировать и закрыть
