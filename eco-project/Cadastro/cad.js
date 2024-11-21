document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const nome = document.getElementById('email').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    // Verifica o elemento
    console.log("Elemento de resposta:", document.getElementById('responseMessage'));

    registerUser(nome,email,senha);
});

function registerUser(nome,email,senha) {
  axios.post('http://127.0.0.1:5000/register', {
    nome: nome,
    email: email,
    senha: senha
  })
  
  .then(response => {
    document.getElementById('responseMessage').innerHTML = `<p style = "color:green">${response.data.message}</p>`;
    console.log("Cadastro realizado com sucesso!!", response.data);

     document.getElementById('senha').value = '';
  })

  .catch(error => {
    let errorMsg = "Erro desconhecido, tente novamente mais tarde";
    if (error.response && error.response.data) {
        errorMsg = error.response.data.message;
    }
    document.getElementById('responseMessage').innerHTML = `<p style="color:red">${errorMsg}</p>`;
    console.error("Erro no login:", error.response);
});
}