// Heatmap visualization utilities

function createCalendarHeatmap(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const today = new Date();
    const yearAgo = new Date(today);
    yearAgo.setFullYear(yearAgo.getFullYear() - 1);

    // Create calendar grid
    const weeks = [];
    let currentDate = new Date(yearAgo);

    while (currentDate <= today) {
        const week = [];
        for (let i = 0; i < 7; i++) {
            const dateStr = currentDate.toISOString().split('T')[0];
            const intensity = data[dateStr] ? data[dateStr].intensity / 5 : 0;

            week.push({
                date: dateStr,
                intensity: intensity,
                count: data[dateStr] ? 1 : 0
            });

            currentDate.setDate(currentDate.getDate() + 1);
        }
        weeks.push(week);
    }

    // Render heatmap
    let html = '<div class="heatmap-grid">';
    weeks.forEach(week => {
        week.forEach(day => {
            const color = `rgba(99, 102, 241, ${day.intensity})`;
            html += `<div class="heatmap-cell" 
                          style="background-color: ${color};" 
                          title="${day.date}: ${day.count} entries"
                          data-date="${day.date}">
                    </div>`;
        });
    });
    html += '</div>';

    container.innerHTML = html;
}
