#base: base.mint

#def body():
    @form.action({{ env.url_for('login') }}).method(POST)
        {{ form.render() }}
        @input.type(submit).value(login)
