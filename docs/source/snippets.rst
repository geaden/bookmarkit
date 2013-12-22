Snippets
========

Handle django form errors via ajax
----------------------------------

Example of how to handle form errors via ajax requests.

Response on errors: `{<field_name_1>: [<error_1>, <error_2>, ...], <field_name_2>: [<error_1>, ...], ...}`

.. code-block:: javascript

    $(".ajax-submit-form").submit(function(event){
            $form = $(this);
            event.preventDefault();
            $form.find(".text-error").remove();
            $.ajax($form.attr('action'), {
                data: $form.serialize(),
                type: 'post',
                statusCode: {
                    400: function(error) {
                        var errors = $.parseJSON(error.responseText);
                        for (field in errors) {
                            $($form.find("#id_" + field).get(0)).after(
                                errors[field].map(function(val){
                                    return '<div class="text-error ' + field + '-field">' + val + '</div>';
                                }).join()
                            );
                        };
                        $form.find("input, textarea, select").one("keypress change", function(){
                            console.log(this);
                            $(this).siblings(".text-error." + this.name + "-field").remove();
                        });
                    },
                    200: function(success) {
                        $form.replaceWith("Success");
                    }
                }
            });

