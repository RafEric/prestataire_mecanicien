
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

        function validateStep2() {
            let isValid = true;
            $('#step2 input[required]').each(function() {
                if (!this.value.trim()) {
                    isValid = false;
                    $(this).addClass('is-invalid');
                } else {
                    $(this).removeClass('is-invalid');
                }
            });
            return isValid;
        }

        $('#next2').click(function() {
            if (validateStep2()) {
                $('#step2').fadeOut(500, function() {
                    $('#step3').fadeIn(500).addClass('active');
                    $(this).removeClass('active');
                });
            }
        });

        $('#prev2').click(function() {
            $('#step3').fadeOut(500, function() {
                $('#step2').fadeIn(500).addClass('active');
                $(this).removeClass('active');
            });
        });

        function togglePrestataireFields() {
            if ($('#user_type').val() === 'prestataire') {
                $('#prestataire_fields').slideDown();
            } else {
                $('#prestataire_fields').slideUp();
            }
        }

        togglePrestataireFields();

        $('#user_type').change(function() {
            togglePrestataireFields();
        });
   

