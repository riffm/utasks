#base: base.mint

#def body():
    @form.action({{ env.url_for('create-issue', proj=project.id) }}).method(POST)
        {{ form.render() }}
        @input.type(submit).value(Создать задачу)
