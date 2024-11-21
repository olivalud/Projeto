function loadLayout() {
    fetch('/eco-project/layout/layout.html')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro ao carregar layout: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('layout').innerHTML = data;

            // Adicionar o css 
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = '/eco-project/layout/layout.css';
            document.head.appendChild(link);

            console.log('Layout carregado com sucesso.');
        })
        .catch(error => console.error('Erro ao carregar o layout:', error));
}

window.onload = loadLayout();


