        document.getElementById('loginForm').addEventListener('submit', function(event) {
            event.preventDefault();  // Impede o envio padrão do formulário

            const email = document.getElementById('email').value;
            const senha = document.getElementById('senha').value;

            console.log("Tentando login...");
            // Verifica o elemento
            console.log("Elemento de resposta:", document.getElementById('responseMessage'));

            // Chama a função para logar o usuário
            loginUser(email, senha);
        });

        function loginUser(email, senha) {
            axios.post('http://127.0.0.1:5000/login', {
                email: email,
                senha: senha
            })
            .then(response => {
                document.getElementById('responseMessage').innerHTML = `<p style="color:green">${response.data.message}</p>`;
                console.log("Login bem-sucedido:", response.data);

                // Limpar o campo de senha após o login bem-sucedido
                document.getElementById('senha').value = '';

                // Aqui você pode redirecionar para outra página ou executar outra ação
                 window.location.href = 'http://127.0.0.1:5500/eco-project/Home/home.html'; 
            })
            .catch(error => {
                let errorMsg = "Erro desconhecido, tente novamente mais tarde... ";
                if (error.response && error.response.data) {
                    errorMsg = error.response.data.message;
                }
                document.getElementById('responseMessage').innerHTML = `<p style="color:red">${errorMsg}</p>`;
                console.error("Erro no login:", error.response);
            });
        }
