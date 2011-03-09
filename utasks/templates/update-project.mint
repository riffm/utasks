#base: base.mint

#def body():
    @form.action({{ env.url_for('update-project', proj=project.id) }}).method(POST)
        {{ form.render() }}
        @input.type(submit).value(Сохранить)
