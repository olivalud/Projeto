document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    try {
      const response  = await axios.post('https:://127.0.0.1:5000/register', {
        email: email,
        password: password
      });

      document.getElementById('response').innerHTML = 'Cadastro realizado com sucesso!';
    }
      catch (error) {
        document.getElementById('response').innerHTML = 'Erro no cadastro' + error.response.data.message;
      }
});