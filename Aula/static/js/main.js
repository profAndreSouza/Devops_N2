// Main JavaScript for Data Science Flask Portal

document.addEventListener('DOMContentLoaded', () => {
    // Inicialização de Tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl));

    // Filtro de Busca na lista de tarefas públicos/dashboard
    const searchInput = document.getElementById('taskSearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.task-item-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});

// Função global para renderizar gráficos Plotly JSON enviados do Flask backend
function renderPlotlyGraph(elementId, plotJson) {
    try {
        const plotData = typeof plotJson === 'string' ? JSON.parse(plotJson) : plotJson;
        Plotly.newPlot(elementId, plotData.data, plotData.layout, {responsive: true, displayModeBar: true});
    } catch (e) {
        console.error("Erro ao renderizar gráfico Plotly:", e);
    }
}
