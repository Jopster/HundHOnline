const statusMessage = document.querySelector('#status-message');
const toolbox = document.querySelector('.toolbox-window');

const actions = {
  'Lizenz / Freischaltung': 'Lizenzverwaltung wurde geöffnet.',
  'CSV - Schnittstelle': 'CSV-Schnittstelle wurde ausgewählt.',
  'SQL-Wizard': 'SQL-Wizard wurde gestartet.',
  'Wartung Datenbank': 'Datenbankwartung wurde ausgewählt.',
  'Wartung Pfade': 'Pfadwartung wurde ausgewählt.',
};

document.querySelectorAll('.module-tabs button').forEach((tab) => {
  tab.addEventListener('click', () => {
    document.querySelector('.module-tabs .active').classList.remove('active');
    tab.classList.add('active');
    document.querySelectorAll('.ribbon-panel').forEach((panel) => {
      panel.hidden = panel.dataset.module !== tab.textContent;
    });
    statusMessage.textContent = `${tab.textContent} wurde ausgewählt.`;
  });
});

document.querySelectorAll('.tabs button').forEach((tab) => {
  tab.addEventListener('click', () => {
    document.querySelector('.tabs .selected').classList.remove('selected');
    tab.classList.add('selected');
    tab.parentElement.querySelectorAll('[role="tab"]').forEach((item) => {
      item.setAttribute('aria-selected', String(item === tab));
    });
    document.querySelectorAll('.toolbox-panel').forEach((panel) => {
      panel.hidden = panel.dataset.panel !== tab.dataset.view;
    });
    statusMessage.textContent = `${tab.textContent} wurde ausgewählt.`;
  });
});

document.querySelectorAll('.utility-actions button').forEach((button) => {
  button.addEventListener('click', () => {
    statusMessage.textContent = actions[button.textContent.trim()];
  });
});

document.querySelector('.close-toolbox').addEventListener('click', () => {
  toolbox.hidden = true;
  statusMessage.textContent = 'Toolbox wurde geschlossen.';
});

document.querySelector('.launch-button').addEventListener('click', () => {
  toolbox.hidden = false;
  statusMessage.textContent = 'Projekte wurden geöffnet.';
});

document.querySelectorAll('.ribbon-command:not(.launch-button)').forEach((button) => {
  button.addEventListener('click', () => {
    statusMessage.textContent = `${button.textContent.trim()} wurde ausgewählt.`;
  });
});

const toolboxTitlebar = document.querySelector('.toolbox-titlebar');
let dragOffsetX = 0;
let dragOffsetY = 0;

toolboxTitlebar.addEventListener('pointerdown', (event) => {
  if (event.target.closest('button')) return;

  const toolboxRect = toolbox.getBoundingClientRect();
  dragOffsetX = event.clientX - toolboxRect.left;
  dragOffsetY = event.clientY - toolboxRect.top;
  toolboxTitlebar.setPointerCapture(event.pointerId);
  toolboxTitlebar.classList.add('dragging');
});

toolboxTitlebar.addEventListener('pointermove', (event) => {
  if (!toolboxTitlebar.hasPointerCapture(event.pointerId)) return;

  const workspaceRect = document.querySelector('.workspace').getBoundingClientRect();
  const maxLeft = Math.max(0, workspaceRect.width - toolbox.offsetWidth);
  const maxTop = Math.max(0, workspaceRect.height - toolbox.offsetHeight);
  const nextLeft = Math.min(maxLeft, Math.max(0, event.clientX - workspaceRect.left - dragOffsetX));
  const nextTop = Math.min(maxTop, Math.max(0, event.clientY - workspaceRect.top - dragOffsetY));
  toolbox.style.left = `${nextLeft}px`;
  toolbox.style.top = `${nextTop}px`;
});

toolboxTitlebar.addEventListener('pointerup', (event) => {
  if (toolboxTitlebar.hasPointerCapture(event.pointerId)) {
    toolboxTitlebar.releasePointerCapture(event.pointerId);
  }
  toolboxTitlebar.classList.remove('dragging');
});
