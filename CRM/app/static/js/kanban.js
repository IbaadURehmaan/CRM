// Select all draggable cards and drop zones (columns)
const cards = document.querySelectorAll('.kanban-card');
const columns = document.querySelectorAll('.kanban-items');

// Add event listeners to cards
cards.forEach(card => {
    card.addEventListener('dragstart', () => {
        card.classList.add('is-dragging');
        // Visual effect while dragging
        card.style.opacity = '0.5';
    });

    card.addEventListener('dragend', () => {
        card.classList.remove('is-dragging');
        card.style.opacity = '1';

        // TODO: Here you can add an AJAX (fetch) call to app/routes.py 
        // to update the new stage in the database automatically.
    });
});

// Enable columns to accept dropped cards
columns.forEach(column => {
    column.addEventListener('dragover', e => {
        e.preventDefault(); // Necessary to allow dropping

        // Find the card currently being dragged
        const draggable = document.querySelector('.is-dragging');

        // Append it to the new column
        column.appendChild(draggable);
    });
});