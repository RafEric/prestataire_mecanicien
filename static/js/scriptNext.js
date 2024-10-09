
        function validateStep1() {
            let isValid = true;
            $('#step1 input[required]').each(function() {
                if (!this.value.trim()) {
                    isValid = false;
                    $(this).addClass('is-invalid');
                } else {
                    $(this).removeClass('is-invalid');
                }
            });
            return isValid;
        }

            $('#next1').click(function() {
                if (validateStep1()) {
                    $('#step1').fadeOut(500, function() {
                        $('#step2').fadeIn(500).addClass('active');
                        $(this).removeClass('active');
                    });
                }
            });

            $('#prev1').click(function() {
                $('#step2').fadeOut(500, function() {
                    $('#step1').fadeIn(500).addClass('active');
                    $(this).removeClass('active');
                });
            });

            