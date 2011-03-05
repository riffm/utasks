#base: base.mint

#def body():
    @form.action({{ env.url_for('create-project') }}).method(POST)
        {{ form.render() }}
        @input.type(submit).value(Создать проект)
