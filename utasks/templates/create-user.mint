#base: base.mint

#def body():
    @form.action({{ env.url_for('create-user') }}).method(POST)
        {{ form.render() }}
        @input.type(submit).value(Добавить пользователя)
