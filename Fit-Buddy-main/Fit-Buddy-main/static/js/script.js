document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       USER LOGIN
    ====================================================== */

    const loginForm = document.getElementById("loginForm");
    const loginButton = document.getElementById("loginBtn");

    if (loginForm) {

        loginForm.addEventListener("submit", function () {

            if (loginButton) {

                loginButton.classList.add("loading");
                loginButton.disabled = true;

                const loginText =
                    loginButton.querySelector("span:first-child");

                if (loginText) {
                    loginText.textContent = "Signing in...";
                }
            }

        });

    }


    /* =====================================================
       ADMIN LOGIN
    ====================================================== */

    const adminLoginForm =
        document.getElementById("adminLoginForm");

    const adminLoginButton =
        document.getElementById("adminLoginBtn");

    if (adminLoginForm) {

        adminLoginForm.addEventListener("submit", function () {

            if (adminLoginButton) {

                adminLoginButton.classList.add("loading");
                adminLoginButton.disabled = true;

                const adminLoginText =
                    adminLoginButton.querySelector("span:first-child");

                if (adminLoginText) {
                    adminLoginText.textContent = "Signing in...";
                }
            }

        });

    }


    /* =====================================================
       REGISTER
    ====================================================== */

    const registerForm =
        document.getElementById("registerForm");

    const registerButton =
        document.getElementById("registerBtn");

    const password =
        document.getElementById("password");

    const confirmPassword =
        document.getElementById("confirm_password");

    const passwordMessage =
        document.getElementById("passwordMessage");


    if (registerForm) {

        function checkPassword() {

            if (
                !password ||
                !confirmPassword ||
                !passwordMessage
            ) {
                return true;
            }


            if (!confirmPassword.value) {

                passwordMessage.textContent = "";

                passwordMessage.classList.remove("show");

                return true;
            }


            if (password.value !== confirmPassword.value) {

                passwordMessage.textContent =
                    "Passwords do not match.";

                passwordMessage.classList.add("show");

                return false;
            }


            passwordMessage.textContent = "";

            passwordMessage.classList.remove("show");

            return true;
        }


        if (password) {
            password.addEventListener(
                "input",
                checkPassword
            );
        }


        if (confirmPassword) {
            confirmPassword.addEventListener(
                "input",
                checkPassword
            );
        }


        registerForm.addEventListener(
            "submit",
            function (event) {

                if (!checkPassword()) {

                    event.preventDefault();

                    if (confirmPassword) {
                        confirmPassword.focus();
                    }

                    return;
                }


                if (registerButton) {

                    registerButton.classList.add("loading");

                    registerButton.disabled = true;

                    const registerText =
                        registerButton.querySelector(
                            "span:first-child"
                        );

                    if (registerText) {
                        registerText.textContent =
                            "Creating account...";
                    }
                }

            }
        );

    }


    /* =====================================================
       FITNESS DASHBOARD
    ====================================================== */

    const fitnessForm =
        document.getElementById("fitnessForm");

    const generateButton =
        document.getElementById("generateBtn");

    const generateText =
        document.getElementById("generateText");


    if (fitnessForm) {

        fitnessForm.addEventListener(
            "submit",
            function () {

                if (generateButton) {

                    generateButton.classList.add("loading");

                    generateButton.disabled = true;

                }


                if (generateText) {

                    generateText.textContent =
                        "Creating Plan...";

                }

            }
        );


        /* ---------------------------------------------
           AGE VALIDATION
        --------------------------------------------- */

        const age =
            document.getElementById("age");


        if (age) {

            age.addEventListener(
                "input",
                function () {

                    if (this.value < 13) {
                        this.value = 13;
                    }

                    if (this.value > 100) {
                        this.value = 100;
                    }

                }
            );

        }


        /* ---------------------------------------------
           HEIGHT VALIDATION
        --------------------------------------------- */

        const height =
            document.getElementById("height");


        if (height) {

            height.addEventListener(
                "input",
                function () {

                    if (this.value < 50) {
                        this.value = 50;
                    }

                    if (this.value > 250) {
                        this.value = 250;
                    }

                }
            );

        }


        /* ---------------------------------------------
           WEIGHT VALIDATION
        --------------------------------------------- */

        const weight =
            document.getElementById("weight");


        if (weight) {

            weight.addEventListener(
                "input",
                function () {

                    if (this.value < 20) {
                        this.value = 20;
                    }

                    if (this.value > 300) {
                        this.value = 300;
                    }

                }
            );

        }

    }

});