/**
 * SwiftPay - lógica do dashboard.
 */

const INITIAL_PAGE = 1;
const PAGE_SIZE = 20;
const INITIAL_FETCH_SIZE = 10000;

const state = {
    currentPage: INITIAL_PAGE,
    perPage: PAGE_SIZE,
    allTransactions: [],
    currentResults: [],
};

const elements = {
    categoryFilter: document.getElementById('category-filter'),
    merchantFilter: document.getElementById('merchant-filter'),
    startDate: document.getElementById('start-date'),
    endDate: document.getElementById('end-date'),
    minAmount: document.getElementById('min-amount'),
    maxAmount: document.getElementById('max-amount'),
    searchBtn: document.getElementById('search-btn'),
    resetBtn: document.getElementById('reset-btn'),
    transactionsBody: document.getElementById('transactions-body'),
    totalTransactions: document.getElementById('total-transactions'),
    totalAmount: document.getElementById('total-amount'),
    averageAmount: document.getElementById('average-amount'),
    maxAmountStat: document.getElementById('max-amount-stat'),
    searchTime: document.getElementById('search-time'),
    resultCount: document.getElementById('result-count'),
    pageInfo: document.getElementById('page-info'),
    prevPage: document.getElementById('prev-page'),
    nextPage: document.getElementById('next-page'),
};

async function init() {
    try {
        await Promise.all([loadCategories(), loadMerchants(), loadStatistics(), loadTransactions()]);
        setupEventListeners();
    } catch (error) {
        console.error('Erro ao inicializar:', error);
        showError('Não foi possível carregar a aplicação');
    }
}

async function loadCategories() {
    const response = await fetch('/api/categories');
    const data = await response.json();

    elements.categoryFilter.innerHTML = '<option value="">Todas as categorias</option>';
    data.categories.forEach((category) => {
        elements.categoryFilter.appendChild(createOption(category));
    });
}

async function loadMerchants() {
    const response = await fetch('/api/merchants');
    const data = await response.json();

    elements.merchantFilter.innerHTML = '<option value="">Todos os merchants</option>';
    data.merchants.forEach((merchant) => {
        elements.merchantFilter.appendChild(createOption(merchant));
    });
}

async function loadTransactions() {
    const response = await fetch(`/api/transactions?page=1&per_page=${INITIAL_FETCH_SIZE}`);
    const data = await response.json();

    state.allTransactions = data.data;
    state.currentResults = data.data;
    state.currentPage = INITIAL_PAGE;
    renderTransactions();
    elements.resultCount.textContent = `Resultados: ${data.total}`;
}

async function loadStatistics() {
    const response = await fetch('/api/statistics');
    const stats = await response.json();
    updateStatistics(stats);
}

async function performSearch() {
    const startedAt = performance.now();

    try {
        const params = new URLSearchParams();
        appendIfPresent(params, 'category', elements.categoryFilter.value);
        appendIfPresent(params, 'merchant', elements.merchantFilter.value);
        appendIfPresent(params, 'start_date', elements.startDate.value);
        appendIfPresent(params, 'end_date', elements.endDate.value);
        appendIfPresent(params, 'min_amount', elements.minAmount.value);
        appendIfPresent(params, 'max_amount', elements.maxAmount.value);

        const response = await fetch(`/api/search?${params.toString()}`);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Falha na busca');
        }

        state.currentResults = data.data;
        state.currentPage = INITIAL_PAGE;
        renderTransactions();
        updateStatistics(data.statistics);

        const elapsed = performance.now() - startedAt;
        elements.searchTime.textContent = `Tempo: ${elapsed.toFixed(2)}ms`;
        elements.resultCount.textContent = `Resultados: ${data.count}`;
    } catch (error) {
        console.error('Erro na busca:', error);
        showError(error.message);
    }
}

function resetFilters() {
    elements.categoryFilter.value = '';
    elements.merchantFilter.value = '';
    elements.startDate.value = '';
    elements.endDate.value = '';
    elements.minAmount.value = '';
    elements.maxAmount.value = '';

    state.currentPage = INITIAL_PAGE;
    state.currentResults = [...state.allTransactions];
    renderTransactions();
    loadStatistics();

    elements.searchTime.textContent = 'Tempo: -';
    elements.resultCount.textContent = `Resultados: ${state.currentResults.length}`;
}

function renderTransactions() {
    const startIndex = (state.currentPage - 1) * state.perPage;
    const endIndex = startIndex + state.perPage;
    const pageTransactions = state.currentResults.slice(startIndex, endIndex);

    if (pageTransactions.length === 0) {
        elements.transactionsBody.innerHTML = '<tr><td colspan="5" class="loading">Nenhuma transação encontrada</td></tr>';
        updatePaginationInfo();
        return;
    }

    elements.transactionsBody.innerHTML = pageTransactions.map((transaction) => `
        <tr>
            <td>${formatDate(transaction.date)}</td>
            <td>${escapeHtml(transaction.merchant)}</td>
            <td>${escapeHtml(transaction.category)}</td>
            <td>${formatCurrency(transaction.amount)}</td>
            <td><span class="status-badge status-${transaction.status.toLowerCase()}">${escapeHtml(transaction.status)}</span></td>
        </tr>
    `).join('');

    updatePaginationInfo();
}

function updatePaginationInfo() {
    const totalPages = Math.max(Math.ceil(state.currentResults.length / state.perPage), 1);
    elements.pageInfo.textContent = `Página ${state.currentPage} de ${totalPages}`;
    elements.prevPage.disabled = state.currentPage <= 1;
    elements.nextPage.disabled = state.currentPage >= totalPages;
}

function updateStatistics(stats) {
    elements.totalTransactions.textContent = Number(stats.total_transactions || 0).toLocaleString('pt-BR');
    elements.totalAmount.textContent = formatCurrency(stats.total_amount || 0);
    elements.averageAmount.textContent = formatCurrency(stats.average_amount || 0);
    elements.maxAmountStat.textContent = formatCurrency(stats.max_amount || 0);
}

function setupEventListeners() {
    elements.searchBtn.addEventListener('click', performSearch);
    elements.resetBtn.addEventListener('click', resetFilters);

    elements.prevPage.addEventListener('click', () => {
        if (state.currentPage > 1) {
            state.currentPage -= 1;
            renderTransactions();
        }
    });

    elements.nextPage.addEventListener('click', () => {
        const totalPages = Math.max(Math.ceil(state.currentResults.length / state.perPage), 1);
        if (state.currentPage < totalPages) {
            state.currentPage += 1;
            renderTransactions();
        }
    });

    [elements.categoryFilter, elements.merchantFilter, elements.startDate, elements.endDate, elements.minAmount, elements.maxAmount]
        .forEach((element) => {
            element.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    performSearch();
                }
            });
        });
}

function appendIfPresent(params, key, value) {
    if (value !== '') {
        params.append(key, value);
    }
}

function createOption(value) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    return option;
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(Number(value || 0));
}

function formatDate(dateString) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(`${dateString}T00:00:00`));
}

function escapeHtml(text) {
    return String(text)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function showError(message) {
    alert(`❌ ${message}`);
}

document.addEventListener('DOMContentLoaded', init);
