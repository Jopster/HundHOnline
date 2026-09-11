const statusMessage = document.querySelector('#status-message');
const toolbox = document.querySelector('.toolbox-window');
const articleList = document.querySelector('.article-window');
const articleDetail = document.querySelector('.article-detail');
const articleGridBody = document.querySelector('#article-grid-body');
const articleSearch = document.querySelector('#article-search');
const groupName = document.querySelector('#group-name');
const articleName = document.querySelector('#article-name');

const articles = [
  ['27', 'Abfallsammler', 'AA 130', 'Abfallsammler für Schränke mit Frontauszug', 'Frank-Michael Stoltenberg', '1', '528,00', '0,00', '19', 'Stück'],
  ['27', 'Abfallsammler', 'AA 131', 'Abfallsammler Unterbau', 'Susanne Schneider', '1', '349,00', '0,00', '19', 'Stück'],
  ['27', 'Auszüge', 'AZ_71', 'Auszug System 71', 'Digital Dynamic', '1', '274,75', '0,00', '19', 'Stück'],
  ['27', 'Auszüge', 'U_TIG_71', 'Unterflurauszug TIG 71', 'Digital Dynamic', '1', '74,11', '0,00', '19', 'Stück'],
  ['27', 'Beschläge', 'TÜR', 'Tür', 'Beschläge Müller', '1', '0,00', '0,00', '19', 'Stück'],
  ['27', 'Arbeitsplatten', 'AP_DESIGN', 'Artikel Designer Gruppe', 'Arbeitsplatten GmbH', '1', '380,13', '0,00', '19', 'Stück'],
];

let activeGroup = 'Alle';
let selectedArticle = articles[0];
let highestWindowLayer = 8;

function bringWindowToFront(windowElement) {
  highestWindowLayer += 1;
  windowElement.style.zIndex = highestWindowLayer;
}

function renderArticles() {
  const query = articleSearch.value.trim().toLocaleLowerCase('de');
  const visibleArticles = articles.filter((article) => (activeGroup === 'Alle' || article[1] === activeGroup || (activeGroup === 'Möbel' && article[1] !== 'Arbeitsplatten')) && article.join(' ').toLocaleLowerCase('de').includes(query));
  articleGridBody.innerHTML = visibleArticles.map((article) => `<tr class="${article === selectedArticle ? 'selected' : ''}" data-number="${article[2]}"><td>${article[0]}</td><td>Artikelmappe</td><td>✓</td><td></td><td>${article[3]}</td><td>${article[4]}</td><td>${article[2]}</td><td>${article[5]}</td><td>${article[6]}</td><td>${article[7]}</td><td>${article[8]}</td><td>${article[9]}</td><td></td></tr>`).join('');
  groupName.textContent = activeGroup;
  articleName.textContent = selectedArticle[3];
}

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
  bringWindowToFront(toolbox);
  statusMessage.textContent = 'Projekte wurden geöffnet.';
});

document.querySelectorAll('.ribbon-command:not(.launch-button)').forEach((button) => {
  button.addEventListener('click', () => {
    statusMessage.textContent = `${button.textContent.trim()} wurde ausgewählt.`;
  });
});

function openArticleList() {
  articleList.hidden = false;
  articleDetail.hidden = true;
  toolbox.hidden = true;
  bringWindowToFront(articleList);
  renderArticles();
  statusMessage.textContent = 'Artikelliste wurde geöffnet.';
}

function openArticleDetail() {
  articleDetail.hidden = false;
  bringWindowToFront(articleDetail);
  statusMessage.textContent = `${selectedArticle[3]} wird bearbeitet.`;
}

document.querySelectorAll('.ribbon-command').forEach((button) => {
  if (button.textContent.trim() === 'Artikel/Texte') button.addEventListener('click', openArticleList);
});

document.querySelectorAll('.close-article-list').forEach((button) => {
  button.addEventListener('click', () => {
    articleList.hidden = true;
    statusMessage.textContent = 'Artikelliste wurde geschlossen.';
  });
});

document.querySelector('.open-article').addEventListener('click', openArticleDetail);
document.querySelector('.print-list').addEventListener('click', () => window.print());

document.querySelectorAll('.tree-node').forEach((node) => {
  node.addEventListener('click', () => {
    document.querySelector('.tree-node.selected').classList.remove('selected');
    node.classList.add('selected');
    activeGroup = node.dataset.group;
    renderArticles();
    statusMessage.textContent = `Warengruppe ${activeGroup} wurde gefiltert.`;
  });
});

articleSearch.addEventListener('input', renderArticles);

articleGridBody.addEventListener('click', (event) => {
  const row = event.target.closest('tr');
  if (!row) return;
  selectedArticle = articles.find((article) => article[2] === row.dataset.number);
  renderArticles();
});

articleGridBody.addEventListener('dblclick', (event) => {
  if (event.target.closest('tr')) openArticleDetail();
});

document.querySelectorAll('.detail-tabs button[data-detail]').forEach((tab) => {
  tab.addEventListener('click', () => {
    document.querySelector('.detail-tabs .active').classList.remove('active');
    tab.classList.add('active');
    document.querySelectorAll('.detail-panel').forEach((panel) => {
      panel.hidden = panel.dataset.detailPanel !== tab.dataset.detail;
    });
  });
});

document.querySelectorAll('.close-article-detail').forEach((button) => {
  button.addEventListener('click', () => {
    articleDetail.hidden = true;
    statusMessage.textContent = 'Artikeldaten wurden geschlossen.';
  });
});

document.querySelector('.save-article').addEventListener('click', () => {
  articleDetail.hidden = true;
  renderArticles();
  statusMessage.textContent = 'Artikeldaten wurden gespeichert.';
});

renderArticles();

function makeWindowInteractive(windowElement, titlebar) {
  const resizeHandle = document.createElement('span');
  resizeHandle.className = 'window-resize-handle';
  resizeHandle.setAttribute('aria-label', 'Fenstergröße ändern');
  windowElement.append(resizeHandle);

  function bringToFront() {
    bringWindowToFront(windowElement);
  }

  function beginPointerAction(event, action) {
    if (action === 'move' && event.target.closest('button')) return;
    bringToFront();
    const pointerTarget = event.currentTarget;
    const workspaceRect = document.querySelector('.workspace').getBoundingClientRect();
    const windowRect = windowElement.getBoundingClientRect();
    const startX = event.clientX;
    const startY = event.clientY;
    const startLeft = windowRect.left - workspaceRect.left;
    const startTop = windowRect.top - workspaceRect.top;
    const startWidth = windowRect.width;
    const startHeight = windowRect.height;
    const minimumWidth = Number.parseFloat(getComputedStyle(windowElement).minWidth) || 320;
    const minimumHeight = Number.parseFloat(getComputedStyle(windowElement).minHeight) || 200;

    event.preventDefault();
    titlebar.classList.toggle('dragging', action === 'move');

    const move = (moveEvent) => {
      if (action === 'move') {
        const maxLeft = Math.max(0, workspaceRect.width - startWidth);
        const maxTop = Math.max(0, workspaceRect.height - startHeight);
        windowElement.style.left = `${Math.min(maxLeft, Math.max(0, startLeft + moveEvent.clientX - startX))}px`;
        windowElement.style.top = `${Math.min(maxTop, Math.max(0, startTop + moveEvent.clientY - startY))}px`;
        return;
      }
      const maximumWidth = workspaceRect.width - startLeft;
      const maximumHeight = workspaceRect.height - startTop;
      windowElement.style.width = `${Math.min(maximumWidth, Math.max(minimumWidth, startWidth + moveEvent.clientX - startX))}px`;
      windowElement.style.height = `${Math.min(maximumHeight, Math.max(minimumHeight, startHeight + moveEvent.clientY - startY))}px`;
    };

    const finish = (finishEvent) => {
      titlebar.classList.remove('dragging');
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', finish);
      window.removeEventListener('pointercancel', finish);
    };

    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', finish);
    window.addEventListener('pointercancel', finish);
  }

  windowElement.addEventListener('pointerdown', bringToFront);
  titlebar.addEventListener('pointerdown', (event) => beginPointerAction(event, 'move'));
  resizeHandle.addEventListener('pointerdown', (event) => beginPointerAction(event, 'resize'));
}

makeWindowInteractive(toolbox, document.querySelector('.toolbox-titlebar'));
makeWindowInteractive(articleList, articleList.querySelector('.article-titlebar'));
makeWindowInteractive(articleDetail, articleDetail.querySelector('.article-titlebar'));
