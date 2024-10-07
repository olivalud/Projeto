document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault(); // Impede o envio padrão do formulário
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();
        const responseDiv = document.getElementById('response');
        responseDiv.innerText = data.message;

        // Se o login for bem-sucedido, redirecione para a página desejada
        if (response.status === 200) {
            window.location.href = '/dashboard'; // Altere para a URL que desejar
        }
    });
});
