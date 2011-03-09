#base: base.mint

#def body():
    @form.action({{ login_url }}).method(POST)
        {{ form.render() }}
        @input.type(submit).value(login)
