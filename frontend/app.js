/**
 * FinancePro - Modern Electron Frontend
 * Main Application JavaScript
 */

// ============================================
// Configuration & State
// ============================================
const API_BASE = 'http://127.0.0.1:8000';
const RETRY_DELAY = 1000;
const MAX_RETRIES = 10;

const state = {
    isAuthenticated: false,
    currentView: 'dashboard',
    clients: [],
    loans: [],
    theme: localStorage.getItem('theme') || 'light',
    sidebarCollapsed: localStorage.getItem('sidebarCollapsed') === 'true'
};

// ============================================
// DOM Elements
// ============================================
const elements = {
    // Screens
    splashScreen: document.getElementById('splash-screen'),
    loginScreen: document.getElementById('login-screen'),
    appContainer: document.getElementById('app-container'),
    
    // Login
    loginForm: document.getElementById('login-form'),
    usernameInput: document.getElementById('username'),
    passwordInput: document.getElementById('password'),
    loginError: document.getElementById('login-error'),
    togglePassword: document.querySelector('.toggle-password'),
    
    // Navigation
    sidebar: document.getElementById('sidebar'),
    sidebarToggle: document.getElementById('sidebar-toggle'),
    navItems: document.querySelectorAll('.nav-item'),
    pageTitle: document.getElementById('page-title'),
    breadcrumb: document.getElementById('breadcrumb'),
    btnLogout: document.getElementById('btn-logout'),
    
    // Header
    globalSearch: document.getElementById('global-search'),
    btnThemeToggle: document.getElementById('btn-theme-toggle'),
    themeIcon: document.getElementById('theme-icon'),
    
    // Views
    views: document.querySelectorAll('.view'),
    
    // Dashboard
    statTotalEmprestado: document.getElementById('stat-total-emprestado'),
    statTotalRecebido: document.getElementById('stat-total-recebido'),
    statAReceber: document.getElementById('stat-a-receber'),
    statAtrasados: document.getElementById('stat-atrasados'),
    recentActivity: document.getElementById('recent-activity'),
    alertsList: document.getElementById('alerts-list'),
    
    // Clients
    clientsCount: document.getElementById('clients-count'),
    clientsSearch: document.getElementById('clients-search'),
    clientsTbody: document.getElementById('clients-tbody'),
    clientsEmpty: document.getElementById('clients-empty'),
    clientsShowing: document.getElementById('clients-showing'),
    clientsTotal: document.getElementById('clients-total'),
    btnNewClient: document.getElementById('btn-new-client'),
    btnAddFirstClient: document.getElementById('btn-add-first-client'),
    
    // Loans
    loansCount: document.getElementById('loans-count'),
    loansSearch: document.getElementById('loans-search'),
    loansGrid: document.getElementById('loans-grid'),
    loansEmpty: document.getElementById('loans-empty'),
    btnNewLoan: document.getElementById('btn-new-loan'),
    btnAddFirstLoan: document.getElementById('btn-add-first-loan'),
    
    // Payments
    paymentForm: document.getElementById('payment-form'),
    paymentLoan: document.getElementById('payment-loan'),
    paymentValue: document.getElementById('payment-value'),
    paymentDate: document.getElementById('payment-date'),
    paymentType: document.getElementById('payment-type'),
    paymentsList: document.getElementById('payments-list'),
    
    // Modal
    modalContainer: document.getElementById('modal-container'),
    modalOverlay: document.getElementById('modal-overlay'),
    modal: document.getElementById('modal'),
    modalTitle: document.getElementById('modal-title'),
    modalBody: document.getElementById('modal-body'),
    modalClose: document.getElementById('modal-close'),
    
    // Toast & Loading
    toastContainer: document.getElementById('toast-container'),
    loadingOverlay: document.getElementById('loading-overlay')
};

// ============================================
// Utility Functions
// ============================================
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value || 0);
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('pt-BR').format(date);
}

function formatDateISO(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toISOString().split('T')[0];
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============================================
// API Functions
// ============================================
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Erro na requisição');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

async function waitForBackend(retries = 0) {
    try {
        const response = await fetch(`${API_BASE}/clients`, { method: 'GET' });
        if (response.ok) return true;
    } catch (e) {
        if (retries < MAX_RETRIES) {
            await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
            return waitForBackend(retries + 1);
        }
    }
    return false;
}

// ============================================
// Toast Notifications
// ============================================
function showToast(message, type = 'info', title = null) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        error: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
        warning: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        info: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
    };
    
    const titles = {
        success: 'Sucesso',
        error: 'Erro',
        warning: 'Atenção',
        info: 'Informação'
    };
    
    toast.innerHTML = `
        <span class="toast-icon">${icons[type]}</span>
        <div class="toast-content">
            <div class="toast-title">${title || titles[type]}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close">×</button>
    `;
    
    elements.toastContainer.appendChild(toast);
    
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => removeToast(toast));
    
    setTimeout(() => removeToast(toast), 5000);
}

function removeToast(toast) {
    toast.style.animation = 'slideInRight 0.3s ease reverse';
    setTimeout(() => toast.remove(), 300);
}

// ============================================
// Loading Overlay
// ============================================
function showLoading() {
    elements.loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

// ============================================
// Modal Functions
// ============================================
function openModal(title, content) {
    elements.modalTitle.innerHTML = title;
    elements.modalBody.innerHTML = content;
    elements.modalContainer.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Focus first input
    const firstInput = elements.modalBody.querySelector('input, select');
    if (firstInput) setTimeout(() => firstInput.focus(), 100);
}

function closeModal() {
    elements.modalContainer.classList.add('hidden');
    document.body.style.overflow = '';
}

// ============================================
// Theme Management
// ============================================
function setTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    elements.themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    
    // Update settings buttons
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === theme);
    });
}

function toggleTheme() {
    setTheme(state.theme === 'dark' ? 'light' : 'dark');
}

// ============================================
// Sidebar Management
// ============================================
function toggleSidebar() {
    state.sidebarCollapsed = !state.sidebarCollapsed;
    elements.sidebar.classList.toggle('collapsed', state.sidebarCollapsed);
    localStorage.setItem('sidebarCollapsed', state.sidebarCollapsed);
}

// ============================================
// Navigation
// ============================================
function navigateTo(viewName) {
    state.currentView = viewName;
    
    // Update nav items
    elements.navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.view === viewName);
    });
    
    // Update views
    elements.views.forEach(view => {
        view.classList.toggle('active', view.id === `view-${viewName}`);
    });
    
    // Update page title
    const titles = {
        dashboard: 'Dashboard',
        clients: 'Clientes',
        loans: 'Empréstimos',
        payments: 'Pagamentos',
        reports: 'Relatórios',
        settings: 'Configurações'
    };
    
    elements.pageTitle.textContent = titles[viewName] || viewName;
    elements.breadcrumb.querySelector('.current').textContent = titles[viewName] || viewName;
    
    // Load view data
    switch (viewName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'clients':
            loadClients();
            break;
        case 'loans':
            loadLoans();
            break;
        case 'payments':
            loadPaymentsView();
            break;
    }
}

// ============================================
// Authentication
// ============================================
async function handleLogin(e) {
    e.preventDefault();
    
    const username = elements.usernameInput.value.trim();
    const password = elements.passwordInput.value;
    
    if (!username || !password) {
        showLoginError('Por favor, preencha todos os campos');
        return;
    }
    
    const btnLogin = elements.loginForm.querySelector('.btn-login');
    const btnText = btnLogin.querySelector('span:first-child');
    const btnLoader = btnLogin.querySelector('.btn-loader');
    
    btnText.textContent = 'Entrando...';
    btnLoader.classList.remove('hidden');
    btnLogin.disabled = true;
    
    try {
        await apiRequest('/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        state.isAuthenticated = true;
        hideLoginError();
        
        // Transition to app
        elements.loginScreen.classList.add('hidden');
        elements.appContainer.classList.remove('hidden');
        
        // Load initial data
        await loadInitialData();
        navigateTo('dashboard');
        
        showToast('Bem-vindo ao FinancePro!', 'success');
        
    } catch (error) {
        showLoginError(error.message || 'Usuário ou senha inválidos');
    } finally {
        btnText.textContent = 'Entrar';
        btnLoader.classList.add('hidden');
        btnLogin.disabled = false;
    }
}

function showLoginError(message) {
    elements.loginError.classList.remove('hidden');
    elements.loginError.querySelector('.error-message').textContent = message;
}

function hideLoginError() {
    elements.loginError.classList.add('hidden');
}

function handleLogout() {
    state.isAuthenticated = false;
    state.clients = [];
    state.loans = [];
    
    elements.appContainer.classList.add('hidden');
    elements.loginScreen.classList.remove('hidden');
    
    // Clear form
    elements.usernameInput.value = '';
    elements.passwordInput.value = '';
    
    showToast('Você foi desconectado', 'info');
}

// ============================================
// Data Loading
// ============================================
async function loadInitialData() {
    showLoading();
    try {
        const [clients, loans] = await Promise.all([
            apiRequest('/clients'),
            apiRequest('/loans')
        ]);
        
        state.clients = clients;
        state.loans = loans;
        
        // Update badges
        elements.clientsCount.textContent = clients.length;
        elements.loansCount.textContent = loans.length;
        
    } catch (error) {
        showToast('Erro ao carregar dados', 'error');
    } finally {
        hideLoading();
    }
}

// ============================================
// Dashboard
// ============================================
async function loadDashboard() {
    try {
        // Calculate stats
        const totalEmprestado = state.loans.reduce((sum, l) => sum + (l.valor_emprestado || 0), 0);
        const totalRecebido = state.loans.reduce((sum, l) => {
            const pagamentos = l.pagamentos || [];
            return sum + pagamentos.reduce((ps, p) => ps + (p.valor || 0), 0);
        }, 0);
        const aReceber = state.loans.reduce((sum, l) => sum + (l.saldo_devedor || 0), 0);
        const atrasados = state.loans.filter(l => {
            if (l.saldo_devedor <= 0) return false;
            const hoje = new Date().toISOString().split('T')[0];
            return l.data_vencimento && hoje > l.data_vencimento;
        }).length;
        
        // Update stats
        elements.statTotalEmprestado.textContent = formatCurrency(totalEmprestado);
        elements.statTotalRecebido.textContent = formatCurrency(totalRecebido);
        elements.statAReceber.textContent = formatCurrency(aReceber);
        elements.statAtrasados.textContent = atrasados;
        
        // Update charts
        renderStatusChart();
        renderEvolutionChart();
        
        // Update recent activity
        renderRecentActivity();
        
        // Update alerts
        renderAlerts();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function renderStatusChart() {
    const ctx = document.getElementById('canvas-status');
    if (!ctx) return;
    
    const quitados = state.loans.filter(l => l.saldo_devedor <= 0).length;
    const emDia = state.loans.filter(l => {
        if (l.saldo_devedor <= 0) return false;
        const hoje = new Date().toISOString().split('T')[0];
        return !l.data_vencimento || hoje <= l.data_vencimento;
    }).length;
    const atrasados = state.loans.filter(l => {
        if (l.saldo_devedor <= 0) return false;
        const hoje = new Date().toISOString().split('T')[0];
        return l.data_vencimento && hoje > l.data_vencimento;
    }).length;
    
    // Destroy existing chart
    if (window.statusChart) window.statusChart.destroy();
    
    window.statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Quitados', 'Em dia', 'Atrasados'],
            datasets: [{
                data: [quitados, emDia, atrasados],
                backgroundColor: ['#10b981', '#3b82f6', '#ef4444'],
                borderWidth: 0,
                spacing: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            },
            cutout: '60%'
        }
    });
}

function renderEvolutionChart() {
    const ctx = document.getElementById('canvas-evolution');
    if (!ctx) return;
    
    // Group loans by month
    const months = {};
    const now = new Date();
    
    for (let i = 5; i >= 0; i--) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
        months[key] = { emprestado: 0, recebido: 0 };
    }
    
    state.loans.forEach(loan => {
        const loanDate = loan.data_emprestimo || loan.data_criacao;
        if (loanDate) {
            const key = loanDate.substring(0, 7);
            if (months[key]) {
                months[key].emprestado += loan.valor_emprestado || 0;
            }
        }
        
        (loan.pagamentos || []).forEach(p => {
            if (p.data) {
                const key = p.data.substring(0, 7);
                if (months[key]) {
                    months[key].recebido += p.valor || 0;
                }
            }
        });
    });
    
    const labels = Object.keys(months).map(k => {
        const [year, month] = k.split('-');
        const monthNames = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
        return monthNames[parseInt(month) - 1];
    });
    
    // Destroy existing chart
    if (window.evolutionChart) window.evolutionChart.destroy();
    
    window.evolutionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Emprestado',
                    data: Object.values(months).map(m => m.emprestado),
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Recebido',
                    data: Object.values(months).map(m => m.recebido),
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => formatCurrency(value)
                    }
                }
            }
        }
    });
}

function renderRecentActivity() {
    const activities = [];
    
    const loanIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>';
    const paymentIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
    
    // Get recent loans
    state.loans.slice(-5).forEach(loan => {
        const client = state.clients.find(c => c.id === loan.cliente_id);
        activities.push({
            type: 'loan',
            icon: loanIcon,
            text: `Empréstimo de ${formatCurrency(loan.valor_emprestado)} para ${client?.nome || 'Cliente'}`,
            date: loan.data_criacao
        });
        
        // Get recent payments
        (loan.pagamentos || []).slice(-3).forEach(p => {
            activities.push({
                type: 'payment',
                icon: paymentIcon,
                text: `Pagamento de ${formatCurrency(p.valor)} recebido`,
                date: p.data
            });
        });
    });
    
    // Sort by date
    activities.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    if (activities.length === 0) {
        elements.recentActivity.innerHTML = `
            <div class="activity-empty">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                <p>Nenhuma atividade recente</p>
            </div>
        `;
        return;
    }
    
    elements.recentActivity.innerHTML = activities.slice(0, 5).map(a => `
        <div class="activity-item">
            <div class="activity-icon">${a.icon}</div>
            <div class="activity-info">
                <div class="activity-text">${a.text}</div>
                <div class="activity-time">${formatDate(a.date)}</div>
            </div>
        </div>
    `).join('');
}

function renderAlerts() {
    const alerts = [];
    
    const warningIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>';
    const checkIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
    
    // Check for overdue loans - usando a lógica correta baseada na parcela atual
    state.loans.forEach(loan => {
        if (loan.saldo_devedor > 0) {
            const loanStatus = calcularStatusEmprestimo(loan);
            if (loanStatus.isOverdue) {
                const client = state.clients.find(c => c.id === loan.cliente_id);
                alerts.push({
                    type: 'danger',
                    icon: warningIcon,
                    text: `Empréstimo de ${client?.nome || 'Cliente'} está ${loanStatus.diasAtraso} dias atrasado`,
                    diasAtraso: loanStatus.diasAtraso
                });
            }
        }
    });
    
    // Ordenar por dias de atraso (mais atrasado primeiro)
    alerts.sort((a, b) => (b.diasAtraso || 0) - (a.diasAtraso || 0));
    
    if (alerts.length === 0) {
        elements.alertsList.innerHTML = `
            <div class="alert-empty">
                ${checkIcon}
                <p>Nenhum alerta no momento</p>
            </div>
        `;
        return;
    }
    
    elements.alertsList.innerHTML = alerts.slice(0, 5).map(a => `
        <div class="alert-item ${a.type}">
            <span class="alert-icon">${a.icon}</span>
            <span class="alert-text">${a.text}</span>
        </div>
    `).join('');
}

// ============================================
// Clients Management
// ============================================
async function loadClients() {
    try {
        state.clients = await apiRequest('/clients');
        renderClients(state.clients);
    } catch (error) {
        showToast('Erro ao carregar clientes', 'error');
    }
}

function renderClients(clients) {
    const userIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>';
    const editIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>';
    const loanIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>';
    
    if (clients.length === 0) {
        elements.clientsTbody.innerHTML = '';
        elements.clientsEmpty.classList.remove('hidden');
        document.getElementById('clients-table').classList.add('hidden');
    } else {
        elements.clientsEmpty.classList.add('hidden');
        document.getElementById('clients-table').classList.remove('hidden');
        
        elements.clientsTbody.innerHTML = clients.map(client => {
            const loansCount = state.loans.filter(l => l.cliente_id === client.id).length;
            return `
                <tr data-id="${client.id}">
                    <td>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <div style="width: 36px; height: 36px; background: var(--bg-tertiary); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--primary);">${userIcon}</div>
                            <div>
                                <div style="font-weight: 600;">${client.nome}</div>
                                <div style="font-size: 0.75rem; color: var(--text-muted);">Cadastrado em ${formatDate(client.data_cadastro)}</div>
                            </div>
                        </div>
                    </td>
                    <td>${client.cpf_cnpj}</td>
                    <td>${client.telefone}</td>
                    <td>${client.email}</td>
                    <td>${loansCount}</td>
                    <td>
                        <span class="status-badge ${client.ativo ? 'active' : 'inactive'}">
                            ${client.ativo ? '● Ativo' : '○ Inativo'}
                        </span>
                    </td>
                    <td class="actions-col">
                        <button class="action-btn edit" onclick="editClient('${client.id}')" title="Editar">${editIcon}</button>
                        <button class="action-btn" onclick="viewClientLoans('${client.id}')" title="Ver empréstimos">${loanIcon}</button>
                    </td>
                </tr>
            `;
        }).join('');
    }
    
    elements.clientsShowing.textContent = clients.length;
    elements.clientsTotal.textContent = state.clients.length;
    elements.clientsCount.textContent = state.clients.length;
}

function filterClients(searchTerm) {
    const term = searchTerm.toLowerCase();
    const filtered = state.clients.filter(c => 
        c.nome.toLowerCase().includes(term) ||
        c.cpf_cnpj.includes(term) ||
        c.email.toLowerCase().includes(term) ||
        c.telefone.includes(term)
    );
    renderClients(filtered);
}

function openNewClientModal() {
    const saveIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>';
    const plusIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>';
    
    const content = `
        <form id="client-form" class="modal-form">
            <div class="form-group">
                <label for="client-nome">Nome completo *</label>
                <input type="text" id="client-nome" required placeholder="Digite o nome completo">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="client-cpf">CPF/CNPJ *</label>
                    <input type="text" id="client-cpf" required placeholder="000.000.000-00">
                </div>
                <div class="form-group">
                    <label for="client-telefone">Telefone *</label>
                    <input type="text" id="client-telefone" required placeholder="(00) 00000-0000">
                </div>
            </div>
            <div class="form-group">
                <label for="client-email">E-mail *</label>
                <input type="email" id="client-email" required placeholder="email@exemplo.com">
            </div>
            <div class="form-group">
                <label for="client-endereco">Endereço</label>
                <input type="text" id="client-endereco" placeholder="Rua, número, bairro, cidade">
            </div>
            <div class="modal-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">Cancelar</button>
                <button type="submit" class="btn-primary">
                    <span>${saveIcon}</span>
                    <span>Salvar Cliente</span>
                </button>
            </div>
        </form>
    `;
    
    openModal(`${plusIcon} Novo Cliente`, content);
    
    document.getElementById('client-form').addEventListener('submit', handleCreateClient);
}

async function handleCreateClient(e) {
    e.preventDefault();
    
    const formData = {
        nome: document.getElementById('client-nome').value.trim(),
        cpf_cnpj: document.getElementById('client-cpf').value.trim(),
        telefone: document.getElementById('client-telefone').value.trim(),
        email: document.getElementById('client-email').value.trim(),
        endereco: document.getElementById('client-endereco').value.trim()
    };
    
    // Validation
    if (!formData.nome || !formData.cpf_cnpj || !formData.telefone || !formData.email) {
        showToast('Preencha todos os campos obrigatórios', 'warning');
        return;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
        showToast('E-mail inválido', 'warning');
        return;
    }
    
    showLoading();
    try {
        await apiRequest('/clients', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        closeModal();
        showToast('Cliente criado com sucesso!', 'success');
        await loadClients();
        
    } catch (error) {
        showToast(error.message || 'Erro ao criar cliente', 'error');
    } finally {
        hideLoading();
    }
}

function editClient(clientId) {
    const client = state.clients.find(c => c.id === clientId);
    if (!client) return;
    
    const saveIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>';
    const editIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>';
    
    const content = `
        <form id="client-form" class="modal-form">
            <div class="form-group">
                <label for="client-nome">Nome completo *</label>
                <input type="text" id="client-nome" required value="${client.nome}">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="client-cpf">CPF/CNPJ *</label>
                    <input type="text" id="client-cpf" required value="${client.cpf_cnpj}">
                </div>
                <div class="form-group">
                    <label for="client-telefone">Telefone *</label>
                    <input type="text" id="client-telefone" required value="${client.telefone}">
                </div>
            </div>
            <div class="form-group">
                <label for="client-email">E-mail *</label>
                <input type="email" id="client-email" required value="${client.email}">
            </div>
            <div class="form-group">
                <label for="client-endereco">Endereço</label>
                <input type="text" id="client-endereco" value="${client.endereco || ''}">
            </div>
            <div class="modal-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">Cancelar</button>
                <button type="submit" class="btn-primary">
                    <span>${saveIcon}</span>
                    <span>Salvar Alterações</span>
                </button>
            </div>
        </form>
    `;
    
    openModal(`${editIcon} Editar Cliente`, content);
    
    document.getElementById('client-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        // Note: API endpoint for update would need to be implemented
        showToast('Funcionalidade de edição em desenvolvimento', 'info');
        closeModal();
    });
}

function viewClientLoans(clientId) {
    const client = state.clients.find(c => c.id === clientId);
    const clientLoans = state.loans.filter(l => l.cliente_id === clientId);
    
    if (clientLoans.length === 0) {
        showToast(`${client?.nome || 'Cliente'} não possui empréstimos`, 'info');
        return;
    }
    
    navigateTo('loans');
    // Filter loans by client
    renderLoans(clientLoans);
}

// ============================================
// Loans Management
// ============================================
async function loadLoans() {
    try {
        state.loans = await apiRequest('/loans');
        renderLoans(state.loans);
    } catch (error) {
        showToast('Erro ao carregar empréstimos', 'error');
    }
}

// Função auxiliar para calcular o status do empréstimo baseado na parcela atual
function calcularStatusEmprestimo(loan) {
    const hoje = new Date();
    
    // Se quitado, retorna status quitado
    if (loan.saldo_devedor <= 0) {
        return {
            status: 'Quitado',
            statusClass: 'paid',
            diasAtraso: 0,
            parcelaAtual: loan.prazo_meses,
            dataVencimentoParcela: null,
            isOverdue: false
        };
    }
    
    // Calcular parcela pendente e data de vencimento
    const parcelasPagas = loan.pagamentos?.length || 0;
    const parcelaAtual = parcelasPagas + 1;
    const dataEmprestimo = new Date(loan.data_emprestimo);
    const dataVencimentoParcela = new Date(dataEmprestimo);
    dataVencimentoParcela.setMonth(dataVencimentoParcela.getMonth() + parcelaAtual);
    
    // Calcular dias de atraso (positivo = atrasado, negativo = dias restantes)
    const diasAtraso = Math.floor((hoje - dataVencimentoParcela) / (1000 * 60 * 60 * 24));
    
    // Determinar status baseado na parcela atual
    if (diasAtraso > 0) {
        return {
            status: 'Atrasado',
            statusClass: 'overdue',
            diasAtraso,
            parcelaAtual,
            dataVencimentoParcela,
            isOverdue: true
        };
    } else {
        return {
            status: 'Em dia',
            statusClass: 'active',
            diasAtraso,
            parcelaAtual,
            dataVencimentoParcela,
            isOverdue: false
        };
    }
}

function renderLoans(loans) {
    if (loans.length === 0) {
        elements.loansGrid.innerHTML = '';
        elements.loansEmpty.classList.remove('hidden');
        elements.loansGrid.classList.add('hidden');
    } else {
        elements.loansEmpty.classList.add('hidden');
        elements.loansGrid.classList.remove('hidden');
        
        elements.loansGrid.innerHTML = loans.map(loan => {
            const client = state.clients.find(c => c.id === loan.cliente_id);
            const hoje = new Date();
            
            // Usar função auxiliar para calcular status
            const loanStatus = calcularStatusEmprestimo(loan);
            const { status, statusClass, diasAtraso, parcelaAtual, dataVencimentoParcela } = loanStatus;
            
            let statusIcon;
            if (statusClass === 'paid') {
                statusIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
            } else if (statusClass === 'overdue') {
                statusIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>';
            } else {
                statusIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';
            }
            
            const progress = loan.valor_total > 0 
                ? ((loan.valor_total - loan.saldo_devedor) / loan.valor_total * 100).toFixed(0)
                : 0;
            
            // Mês de referência da parcela
            const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
            const mesReferencia = dataVencimentoParcela ? meses[dataVencimentoParcela.getMonth()] : '';
            const anoReferencia = dataVencimentoParcela ? dataVencimentoParcela.getFullYear() : '';
            
            // Renderizar informação da parcela pendente
            let pendingInfoHtml = '';
            if (loan.saldo_devedor > 0) {
                const pendingClass = diasAtraso > 0 ? 'overdue' : (diasAtraso > -7 ? '' : 'paid');
                const pendingLabel = diasAtraso > 0 ? `${diasAtraso} dias atrasado` : (diasAtraso === 0 ? 'Vence hoje' : `Vence em ${Math.abs(diasAtraso)} dias`);
                const pendingIcon = diasAtraso > 0 
                    ? '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
                    : '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>';
                
                pendingInfoHtml = `
                    <div class="loan-pending-info ${pendingClass}">
                        <div class="loan-pending-header">
                            <span class="loan-pending-label">${pendingIcon} Parcela ${parcelaAtual}/${loan.prazo_meses}</span>
                            <span class="loan-pending-month">${mesReferencia}/${anoReferencia}</span>
                        </div>
                        <div class="loan-pending-value">${formatCurrency(loan.valor_parcela)}</div>
                        <div class="loan-pending-due">${pendingLabel}</div>
                    </div>
                `;
            }
            
            const userIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>';
            const payIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
            const detailsIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>';
            
            return `
                <div class="loan-card" data-id="${loan.id}">
                    <div class="loan-header">
                        <div class="loan-client">
                            <div class="loan-avatar">${userIcon}</div>
                            <div class="loan-client-info">
                                <h4>${client?.nome || 'Cliente'}</h4>
                                <span>${loan.id}</span>
                            </div>
                        </div>
                        <span class="loan-status ${statusClass}">${statusIcon} ${status}</span>
                    </div>
                    
                    ${pendingInfoHtml}
                    
                    <div class="loan-details">
                        <div class="loan-detail">
                            <span class="loan-detail-label">Valor Emprestado</span>
                            <span class="loan-detail-value">${formatCurrency(loan.valor_emprestado)}</span>
                        </div>
                        <div class="loan-detail">
                            <span class="loan-detail-label">Saldo Devedor</span>
                            <span class="loan-detail-value">${formatCurrency(loan.saldo_devedor)}</span>
                        </div>
                        <div class="loan-detail">
                            <span class="loan-detail-label">Taxa de Juros</span>
                            <span class="loan-detail-value">${(loan.taxa_juros * 100).toFixed(1)}% a.m.</span>
                        </div>
                        <div class="loan-detail">
                            <span class="loan-detail-label">Parcelas</span>
                            <span class="loan-detail-value">${loan.prazo_meses}x de ${formatCurrency(loan.valor_parcela)}</span>
                        </div>
                    </div>
                    
                    <div class="loan-progress">
                        <div class="progress-header">
                            <span class="progress-label">Progresso</span>
                            <span class="progress-percent">${progress}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%"></div>
                        </div>
                    </div>
                    
                    <div class="loan-actions">
                        ${loan.saldo_devedor > 0 ? `
                            <button class="loan-btn primary" onclick="openPaymentModal('${loan.id}')">
                                ${payIcon} Pagar
                            </button>
                        ` : ''}
                        <button class="loan-btn secondary" onclick="viewLoanDetails('${loan.id}')">
                            ${detailsIcon} Detalhes
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    elements.loansCount.textContent = state.loans.length;
}

function filterLoans(filter) {
    let filtered = [...state.loans];
    
    switch (filter) {
        case 'active':
            // Empréstimos em dia: saldo devedor > 0 e parcela atual NÃO atrasada
            filtered = filtered.filter(l => {
                if (l.saldo_devedor <= 0) return false;
                const status = calcularStatusEmprestimo(l);
                return !status.isOverdue;
            });
            break;
        case 'overdue':
            // Empréstimos atrasados: saldo devedor > 0 e parcela atual atrasada
            filtered = filtered.filter(l => {
                if (l.saldo_devedor <= 0) return false;
                const status = calcularStatusEmprestimo(l);
                return status.isOverdue;
            });
            break;
        case 'paid':
            filtered = filtered.filter(l => l.saldo_devedor <= 0);
            break;
    }
    
    renderLoans(filtered);
}

function openNewLoanModal() {
    if (state.clients.length === 0) {
        showToast('Cadastre um cliente primeiro', 'warning');
        return;
    }
    
    const clientOptions = state.clients.map(c => 
        `<option value="${c.id}">${c.nome} - ${c.cpf_cnpj}</option>`
    ).join('');
    
    const cardIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>';
    const plusIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>';
    
    const content = `
        <form id="loan-form" class="modal-form">
            <div class="form-group">
                <label for="loan-cliente">Cliente *</label>
                <select id="loan-cliente" required>
                    <option value="">Selecione um cliente</option>
                    ${clientOptions}
                </select>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="loan-valor">Valor do Empréstimo *</label>
                    <div class="input-wrapper">
                        <span class="input-prefix">R$</span>
                        <input type="text" id="loan-valor" required placeholder="0,00" style="padding-left: 2.5rem;">
                    </div>
                </div>
                <div class="form-group">
                    <label for="loan-taxa">Taxa de Juros (% a.m.) *</label>
                    <input type="number" id="loan-taxa" required step="0.01" min="0" placeholder="5.00">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="loan-prazo">Prazo (meses) *</label>
                    <input type="number" id="loan-prazo" required min="1" max="120" placeholder="12">
                </div>
                <div class="form-group">
                    <label for="loan-data">Data do Empréstimo *</label>
                    <input type="date" id="loan-data" required value="${new Date().toISOString().split('T')[0]}">
                </div>
            </div>
            
            <div id="loan-preview" style="padding: 1rem; background: var(--bg-tertiary); border-radius: var(--radius); margin-top: 1rem;">
                <div style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 0.5rem;">Preencha os valores para ver a simulação</div>
            </div>
            
            <div class="modal-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">Cancelar</button>
                <button type="submit" class="btn-primary">
                    <span>${cardIcon}</span>
                    <span>Criar Empréstimo</span>
                </button>
            </div>
        </form>
    `;
    
    openModal(`${plusIcon} Novo Empréstimo`, content);
    
    // Add preview calculation
    const valorInput = document.getElementById('loan-valor');
    const taxaInput = document.getElementById('loan-taxa');
    const prazoInput = document.getElementById('loan-prazo');
    const preview = document.getElementById('loan-preview');
    
    function updatePreview() {
        const valor = parseFloat(valorInput.value.replace(/[^\d,]/g, '').replace(',', '.')) || 0;
        const taxa = parseFloat(taxaInput.value) || 0;
        const prazo = parseInt(prazoInput.value) || 0;
        
        if (valor > 0 && taxa >= 0 && prazo > 0) {
            const total = valor * Math.pow(1 + (taxa / 100), prazo);
            const parcela = total / prazo;
            const juros = total - valor;
            
            preview.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; text-align: center;">
                    <div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem;">VALOR TOTAL</div>
                        <div style="font-size: 1.125rem; font-weight: 700; color: var(--primary);">${formatCurrency(total)}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem;">PARCELA</div>
                        <div style="font-size: 1.125rem; font-weight: 700; color: var(--success);">${formatCurrency(parcela)}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem;">JUROS</div>
                        <div style="font-size: 1.125rem; font-weight: 700; color: var(--warning);">${formatCurrency(juros)}</div>
                    </div>
                </div>
            `;
        }
    }
    
    valorInput.addEventListener('input', updatePreview);
    taxaInput.addEventListener('input', updatePreview);
    prazoInput.addEventListener('input', updatePreview);
    
    document.getElementById('loan-form').addEventListener('submit', handleCreateLoan);
}

async function handleCreateLoan(e) {
    e.preventDefault();
    
    const valor = parseFloat(document.getElementById('loan-valor').value.replace(/[^\d,]/g, '').replace(',', '.')) || 0;
    const taxa = parseFloat(document.getElementById('loan-taxa').value) || 0;
    const prazo = parseInt(document.getElementById('loan-prazo').value) || 0;
    
    const formData = {
        cliente_id: document.getElementById('loan-cliente').value,
        valor_emprestado: valor,
        taxa_juros: taxa,
        prazo_meses: prazo,
        data_emprestimo: document.getElementById('loan-data').value,
        metodo_calculo: 'compostos'
    };
    
    // Validation
    if (!formData.cliente_id) {
        showToast('Selecione um cliente', 'warning');
        return;
    }
    
    if (formData.valor_emprestado <= 0) {
        showToast('O valor do empréstimo deve ser maior que zero', 'warning');
        return;
    }
    
    if (formData.prazo_meses <= 0) {
        showToast('O prazo deve ser maior que zero', 'warning');
        return;
    }
    
    showLoading();
    try {
        await apiRequest('/loans', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        closeModal();
        showToast('Empréstimo criado com sucesso!', 'success');
        await loadLoans();
        await loadInitialData(); // Refresh all data
        
    } catch (error) {
        showToast(error.message || 'Erro ao criar empréstimo', 'error');
    } finally {
        hideLoading();
    }
}

function viewLoanDetails(loanId) {
    const loan = state.loans.find(l => l.id === loanId);
    if (!loan) return;
    
    const client = state.clients.find(c => c.id === loan.cliente_id);
    const hoje = new Date().toISOString().split('T')[0];
    
    // SVG Icons
    const checkCircleIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
    const warningIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>';
    const clockIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';
    const userIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>';
    const moneyIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
    const historyIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>';
    const fileIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>';
    
    // Usar função auxiliar para calcular status correto
    const loanStatus = calcularStatusEmprestimo(loan);
    let status = loanStatus.status;
    let statusClass = loanStatus.statusClass;
    let statusIcon;
    
    if (statusClass === 'paid') {
        statusIcon = checkCircleIcon;
    } else if (statusClass === 'overdue') {
        statusIcon = warningIcon;
    } else {
        statusIcon = clockIcon;
    }
    
    const pagamentos = loan.pagamentos || [];
    const pagamentosHtml = pagamentos.length > 0 
        ? pagamentos.map(p => `
            <div class="payment-item">
                <div class="payment-info">
                    <div class="payment-icon" style="color: var(--success);">${moneyIcon}</div>
                    <div class="payment-details">
                        <h4>${p.tipo || 'Pagamento'}</h4>
                        <span>${formatDate(p.data)}</span>
                    </div>
                </div>
                <div class="payment-amount">${formatCurrency(p.valor)}</div>
            </div>
        `).join('')
        : '<p style="text-align: center; color: var(--text-muted); padding: 1rem;">Nenhum pagamento registrado</p>';
    
    const content = `
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="width: 48px; height: 48px; background: var(--bg-tertiary); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--primary);">${userIcon}</div>
                    <div>
                        <h3 style="font-size: 1.125rem; font-weight: 600;">${client?.nome || 'Cliente'}</h3>
                        <span style="font-size: 0.875rem; color: var(--text-muted);">${loan.id}</span>
                    </div>
                </div>
                <span class="status-badge ${statusClass}">${statusIcon} ${status}</span>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; padding: 1rem; background: var(--bg-tertiary); border-radius: var(--radius); margin-bottom: 1.5rem;">
            <div>
                <div style="font-size: 0.6875rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem;">Valor Emprestado</div>
                <div style="font-size: 1rem; font-weight: 600;">${formatCurrency(loan.valor_emprestado)}</div>
            </div>
            <div>
                <div style="font-size: 0.6875rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem;">Valor Total</div>
                <div style="font-size: 1rem; font-weight: 600;">${formatCurrency(loan.valor_total)}</div>
            </div>
            <div>
                <div style="font-size: 0.6875rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem;">Saldo Devedor</div>
                <div style="font-size: 1rem; font-weight: 600; color: ${loan.saldo_devedor > 0 ? 'var(--danger)' : 'var(--success)'};">${formatCurrency(loan.saldo_devedor)}</div>
            </div>
            <div>
                <div style="font-size: 0.6875rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem;">Taxa de Juros</div>
                <div style="font-size: 1rem; font-weight: 600;">${(loan.taxa_juros * 100).toFixed(2)}% a.m.</div>
            </div>
            <div>
                <div style="font-size: 0.6875rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem;">Parcela</div>
                <div style="font-size: 1rem; font-weight: 600;">${formatCurrency(loan.valor_parcela)}</div>
            </div>
            <div>
                <div style="font-size: 0.6875rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem;">Prazo</div>
                <div style="font-size: 1rem; font-weight: 600;">${loan.prazo_meses} meses</div>
            </div>
            <div>
                <div style="font-size: 0.6875rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem;">Data do Empréstimo</div>
                <div style="font-size: 1rem; font-weight: 600;">${formatDate(loan.data_emprestimo)}</div>
            </div>
            <div>
                <div style="font-size: 0.6875rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem;">Vencimento</div>
                <div style="font-size: 1rem; font-weight: 600;">${formatDate(loan.data_vencimento)}</div>
            </div>
        </div>
        
        <div>
            <h4 style="font-size: 0.875rem; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">${historyIcon} Histórico de Pagamentos</h4>
            <div style="max-height: 200px; overflow-y: auto; border: 1px solid var(--border-color); border-radius: var(--radius);">
                ${pagamentosHtml}
            </div>
        </div>
        
        <div class="modal-actions">
            <button type="button" class="btn-secondary" onclick="closeModal()">Fechar</button>
            ${loan.saldo_devedor > 0 ? `
                <button type="button" class="btn-primary" onclick="closeModal(); openPaymentModal('${loan.id}')">
                    <span>${moneyIcon}</span>
                    <span>Registrar Pagamento</span>
                </button>
            ` : ''}
        </div>
    `;
    
    openModal(`${fileIcon} Detalhes do Empréstimo`, content);
}

// ============================================
// Payments
// ============================================
function loadPaymentsView() {
    // Populate loan select
    const activeLoans = state.loans.filter(l => l.saldo_devedor > 0);
    
    elements.paymentLoan.innerHTML = `
        <option value="">Selecione um empréstimo</option>
        ${activeLoans.map(loan => {
            const client = state.clients.find(c => c.id === loan.cliente_id);
            return `<option value="${loan.id}">${client?.nome || 'Cliente'} - ${formatCurrency(loan.saldo_devedor)} restante</option>`;
        }).join('')}
    `;
    
    // Set today's date
    elements.paymentDate.value = new Date().toISOString().split('T')[0];
    
    // Render payments history
    renderPaymentsHistory();
}

function renderPaymentsHistory() {
    const allPayments = [];
    const moneyIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
    const emptyIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>';
    
    state.loans.forEach(loan => {
        const client = state.clients.find(c => c.id === loan.cliente_id);
        (loan.pagamentos || []).forEach(p => {
            allPayments.push({
                ...p,
                clientName: client?.nome || 'Cliente',
                loanId: loan.id
            });
        });
    });
    
    // Sort by date descending
    allPayments.sort((a, b) => new Date(b.data) - new Date(a.data));
    
    if (allPayments.length === 0) {
        elements.paymentsList.innerHTML = `
            <div class="payments-empty">
                ${emptyIcon}
                <p>Nenhum pagamento registrado</p>
            </div>
        `;
        return;
    }
    
    elements.paymentsList.innerHTML = allPayments.slice(0, 20).map(p => `
        <div class="payment-item">
            <div class="payment-info">
                <div class="payment-icon" style="color: var(--success);">${moneyIcon}</div>
                <div class="payment-details">
                    <h4>${p.clientName}</h4>
                    <span>${formatDate(p.data)} • ${p.tipo || 'Pagamento'}</span>
                </div>
            </div>
            <div class="payment-amount">${formatCurrency(p.valor)}</div>
        </div>
    `).join('');
}

function openPaymentModal(loanId) {
    const loan = state.loans.find(l => l.id === loanId);
    if (!loan) return;
    
    const client = state.clients.find(c => c.id === loan.cliente_id);
    
    const userIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>';
    const moneyIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
    const payIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
    
    const content = `
        <div style="padding: 1rem; background: var(--bg-tertiary); border-radius: var(--radius); margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <div style="width: 40px; height: 40px; background: var(--bg-secondary); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--primary);">${userIcon}</div>
                <div>
                    <div style="font-weight: 600;">${client?.nome || 'Cliente'}</div>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">${loan.id}</div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.875rem;">
                <span>Saldo devedor:</span>
                <span style="font-weight: 600; color: var(--danger);">${formatCurrency(loan.saldo_devedor)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.875rem; margin-top: 0.25rem;">
                <span>Valor da parcela:</span>
                <span style="font-weight: 600;">${formatCurrency(loan.valor_parcela)}</span>
            </div>
        </div>
        
        <form id="payment-modal-form" class="modal-form">
            <div class="form-row">
                <div class="form-group">
                    <label for="modal-payment-valor">Valor do Pagamento *</label>
                    <div class="input-wrapper">
                        <span class="input-prefix">R$</span>
                        <input type="text" id="modal-payment-valor" required placeholder="0,00" value="${loan.valor_parcela.toFixed(2)}" style="padding-left: 2.5rem;">
                    </div>
                </div>
                <div class="form-group">
                    <label for="modal-payment-data">Data *</label>
                    <input type="date" id="modal-payment-data" required value="${new Date().toISOString().split('T')[0]}">
                </div>
            </div>
            <div class="form-group">
                <label for="modal-payment-tipo">Tipo</label>
                <select id="modal-payment-tipo">
                    <option value="Parcela">Parcela</option>
                    <option value="Adiantamento">Adiantamento</option>
                    <option value="Quitação">Quitação Total</option>
                </select>
            </div>
            
            <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                <button type="button" class="btn-secondary" style="flex: 1;" onclick="document.getElementById('modal-payment-valor').value = '${loan.valor_parcela.toFixed(2)}'">
                    1 Parcela
                </button>
                <button type="button" class="btn-secondary" style="flex: 1;" onclick="document.getElementById('modal-payment-valor').value = '${loan.saldo_devedor.toFixed(2)}'; document.getElementById('modal-payment-tipo').value = 'Quitação'">
                    Quitar Tudo
                </button>
            </div>
            
            <div class="modal-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">Cancelar</button>
                <button type="submit" class="btn-primary">
                    <span>${moneyIcon}</span>
                    <span>Confirmar Pagamento</span>
                </button>
            </div>
        </form>
    `;
    
    openModal(`${payIcon} Registrar Pagamento`, content);
    
    document.getElementById('payment-modal-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const valor = parseFloat(document.getElementById('modal-payment-valor').value.replace(/[^\d,]/g, '').replace(',', '.')) || 0;
        const data = document.getElementById('modal-payment-data').value;
        const tipo = document.getElementById('modal-payment-tipo').value;
        
        if (valor <= 0) {
            showToast('O valor deve ser maior que zero', 'warning');
            return;
        }
        
        showLoading();
        try {
            await apiRequest('/payments', {
                method: 'POST',
                body: JSON.stringify({
                    emprestimo_id: loanId,
                    valor,
                    data,
                    tipo
                })
            });
            
            closeModal();
            showToast('Pagamento registrado com sucesso!', 'success');
            await loadInitialData();
            
            if (state.currentView === 'loans') {
                loadLoans();
            } else if (state.currentView === 'payments') {
                loadPaymentsView();
            } else if (state.currentView === 'dashboard') {
                loadDashboard();
            }
            
        } catch (error) {
            showToast(error.message || 'Erro ao registrar pagamento', 'error');
        } finally {
            hideLoading();
        }
    });
}

// ============================================
// Event Listeners
// ============================================
function initEventListeners() {
    // Login
    elements.loginForm.addEventListener('submit', handleLogin);
    
    elements.togglePassword?.addEventListener('click', () => {
        const type = elements.passwordInput.type === 'password' ? 'text' : 'password';
        elements.passwordInput.type = type;
        const eyeOpen = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
        const eyeClosed = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>';
        elements.togglePassword.innerHTML = type === 'password' ? eyeOpen : eyeClosed;
    });
    
    // Navigation
    elements.navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(item.dataset.view);
        });
    });
    
    // Sidebar toggle
    elements.sidebarToggle?.addEventListener('click', toggleSidebar);
    
    // Sidebar expand trigger (for collapsed state)
    const sidebarExpandTrigger = document.getElementById('sidebar-expand-trigger');
    sidebarExpandTrigger?.addEventListener('click', () => {
        if (state.sidebarCollapsed) {
            toggleSidebar();
        }
    });
    
    // Theme toggle
    elements.btnThemeToggle?.addEventListener('click', toggleTheme);
    
    // Logout
    elements.btnLogout?.addEventListener('click', handleLogout);
    
    // Modal
    elements.modalClose?.addEventListener('click', closeModal);
    elements.modalOverlay?.addEventListener('click', closeModal);
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !elements.modalContainer.classList.contains('hidden')) {
            closeModal();
        }
    });
    
    // Clients
    elements.btnNewClient?.addEventListener('click', openNewClientModal);
    elements.btnAddFirstClient?.addEventListener('click', openNewClientModal);
    
    elements.clientsSearch?.addEventListener('input', debounce((e) => {
        filterClients(e.target.value);
    }, 300));
    
    // Loans
    elements.btnNewLoan?.addEventListener('click', openNewLoanModal);
    elements.btnAddFirstLoan?.addEventListener('click', openNewLoanModal);
    
    elements.loansSearch?.addEventListener('input', debounce((e) => {
        const term = e.target.value.toLowerCase();
        const filtered = state.loans.filter(l => {
            const client = state.clients.find(c => c.id === l.cliente_id);
            return l.id.toLowerCase().includes(term) || 
                   (client?.nome || '').toLowerCase().includes(term);
        });
        renderLoans(filtered);
    }, 300));
    
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const parent = e.target.closest('.filter-buttons');
            parent.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            const filter = e.target.dataset.filter;
            const view = state.currentView;
            
            if (view === 'clients') {
                let filtered = [...state.clients];
                if (filter === 'active') filtered = filtered.filter(c => c.ativo);
                if (filter === 'inactive') filtered = filtered.filter(c => !c.ativo);
                renderClients(filtered);
            } else if (view === 'loans') {
                filterLoans(filter);
            }
        });
    });
    
    // Payments form
    elements.paymentForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const loanId = elements.paymentLoan.value;
        const valor = parseFloat(elements.paymentValue.value.replace(/[^\d,]/g, '').replace(',', '.')) || 0;
        const data = elements.paymentDate.value;
        const tipo = elements.paymentType.value;
        
        if (!loanId) {
            showToast('Selecione um empréstimo', 'warning');
            return;
        }
        
        if (valor <= 0) {
            showToast('O valor deve ser maior que zero', 'warning');
            return;
        }
        
        showLoading();
        try {
            await apiRequest('/payments', {
                method: 'POST',
                body: JSON.stringify({
                    emprestimo_id: loanId,
                    valor,
                    data,
                    tipo
                })
            });
            
            showToast('Pagamento registrado com sucesso!', 'success');
            
            // Reset form
            elements.paymentLoan.value = '';
            elements.paymentValue.value = '';
            
            await loadInitialData();
            loadPaymentsView();
            
        } catch (error) {
            showToast(error.message || 'Erro ao registrar pagamento', 'error');
        } finally {
            hideLoading();
        }
    });
    
    // Settings theme buttons
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            setTheme(btn.dataset.theme);
        });
    });
    
    // Global search
    elements.globalSearch?.addEventListener('input', (e) => {
        const term = e.target.value.trim();
        const clearBtn = document.getElementById('search-clear');
        
        // Show/hide clear button
        if (term) {
            clearBtn?.classList.remove('hidden');
        } else {
            clearBtn?.classList.add('hidden');
        }
    });
    
    // Clear search button
    document.getElementById('search-clear')?.addEventListener('click', () => {
        elements.globalSearch.value = '';
        document.getElementById('search-clear').classList.add('hidden');
        elements.globalSearch.focus();
    });
    
    // Notifications button
    document.getElementById('btn-notifications')?.addEventListener('click', () => {
        navigateTo('dashboard');
        // Scroll to alerts section
        setTimeout(() => {
            const alertsSection = document.getElementById('alerts-list');
            alertsSection?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    });
    
    // Payment type - auto fill value
    elements.paymentType?.addEventListener('change', (e) => {
        const loanId = elements.paymentLoan.value;
        if (!loanId) return;
        
        const loan = state.loans.find(l => l.id === loanId);
        if (!loan) return;
        
        const tipo = e.target.value;
        let valor = 0;
        
        if (tipo === 'parcela') {
            valor = loan.valor_parcela;
        } else if (tipo === 'quitacao') {
            valor = loan.saldo_devedor;
        }
        
        if (valor > 0) {
            elements.paymentValue.value = formatCurrency(valor);
        }
    });
}

// ============================================
// Backup Functions
// ============================================
async function createBackup() {
    showLoading();
    
    try {
        const hoje = new Date().toISOString().split('T')[0];
        const hora = new Date().toTimeString().split(' ')[0].replace(/:/g, '');
        const backup = {
            exportDate: new Date().toISOString(),
            version: '2.0.0',
            clients: state.clients,
            loans: state.loans
        };
        
        const result = await window.electronAPI.showSaveDialog({
            title: 'Criar Backup',
            defaultPath: `financepro_backup_${hoje}_${hora}.json`,
            filters: [
                { name: 'Backup JSON', extensions: ['json'] },
                { name: 'Todos os Arquivos', extensions: ['*'] }
            ]
        });
        
        if (!result.canceled && result.filePath) {
            const content = JSON.stringify(backup, null, 2);
            const saveResult = await window.electronAPI.saveFile(result.filePath, content, 'utf8');
            if (saveResult.success) {
                showToast('Backup criado com sucesso!', 'success');
            } else {
                showToast(`Erro ao criar backup: ${saveResult.error}`, 'error');
            }
        }
    } catch (error) {
        showToast('Erro ao criar backup', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function restoreBackup() {
    showToast('Funcionalidade de restauração em desenvolvimento', 'info');
}

// ============================================
// Initialization
// ============================================
async function init() {
    // Apply saved theme
    setTheme(state.theme);
    
    // Apply sidebar state
    if (state.sidebarCollapsed) {
        elements.sidebar.classList.add('collapsed');
    }
    
    // Init event listeners
    initEventListeners();
    
    // Wait for backend
    const backendReady = await waitForBackend();
    
    // Hide splash screen
    setTimeout(() => {
        elements.splashScreen.classList.add('fade-out');
        setTimeout(() => {
            elements.splashScreen.classList.add('hidden');
            
            if (!backendReady) {
                showToast('Não foi possível conectar ao servidor. Verifique se o backend está rodando.', 'error');
            }
            
            // Show login
            elements.loginScreen.classList.remove('hidden');
            elements.usernameInput.focus();
        }, 500);
    }, 2000);
}

// Start application
document.addEventListener('DOMContentLoaded', init);

// ============================================
// Reports & Export Functions
// ============================================
async function generateReport(type) {
    const reportNames = {
        general: 'Relatório Geral',
        overdue: 'Empréstimos Atrasados',
        income: 'Receitas',
        clients: 'Relatório de Clientes',
        monthly: 'Relatório Mensal'
    };
    
    const reportName = reportNames[type] || 'Relatório';
    showLoading();
    
    try {
        let content = '';
        const hoje = new Date();
        const dataFormatada = hoje.toLocaleDateString('pt-BR');
        const horaFormatada = hoje.toLocaleTimeString('pt-BR');
        
        // Header
        content += `FINANCEPRO - ${reportName.toUpperCase()}\n`;
        content += `Gerado em: ${dataFormatada} às ${horaFormatada}\n`;
        content += '='.repeat(60) + '\n\n';
        
        if (type === 'general') {
            content += 'RESUMO GERAL\n';
            content += '-'.repeat(40) + '\n';
            const totalEmprestado = state.loans.reduce((sum, l) => sum + (l.valor_emprestimo || 0), 0);
            const totalRecebido = state.loans.reduce((sum, l) => sum + (l.total_pago || 0), 0);
            const totalAReceber = state.loans.reduce((sum, l) => sum + (l.saldo_devedor || 0), 0);
            content += `Total Emprestado: ${formatCurrency(totalEmprestado)}\n`;
            content += `Total Recebido: ${formatCurrency(totalRecebido)}\n`;
            content += `Total a Receber: ${formatCurrency(totalAReceber)}\n`;
            content += `Total de Clientes: ${state.clients.length}\n`;
            content += `Total de Empréstimos: ${state.loans.length}\n\n`;
            
            content += 'LISTA DE EMPRÉSTIMOS\n';
            content += '-'.repeat(40) + '\n';
            state.loans.forEach(loan => {
                const client = state.clients.find(c => c.id === loan.cliente_id);
                content += `• ${client?.nome || 'N/A'} - ${formatCurrency(loan.valor_emprestimo)} (${loan.prazo_meses}x)\n`;
            });
            
        } else if (type === 'overdue') {
            content += 'EMPRÉSTIMOS EM ATRASO\n';
            content += '-'.repeat(40) + '\n';
            const atrasados = state.loans.filter(loan => {
                const status = calcularStatusEmprestimo(loan);
                return status.isOverdue;
            });
            
            if (atrasados.length === 0) {
                content += 'Nenhum empréstimo em atraso.\n';
            } else {
                atrasados.forEach(loan => {
                    const client = state.clients.find(c => c.id === loan.cliente_id);
                    const status = calcularStatusEmprestimo(loan);
                    content += `• ${client?.nome || 'N/A'}\n`;
                    content += `  Valor: ${formatCurrency(loan.valor_emprestimo)}\n`;
                    content += `  Saldo Devedor: ${formatCurrency(loan.saldo_devedor)}\n`;
                    content += `  Dias em atraso: ${status.diasAtraso}\n`;
                    content += `  Telefone: ${client?.telefone || 'N/A'}\n\n`;
                });
            }
            
        } else if (type === 'income') {
            content += 'ANÁLISE DE RECEITAS\n';
            content += '-'.repeat(40) + '\n';
            const totalRecebido = state.loans.reduce((sum, l) => sum + (l.total_pago || 0), 0);
            const jurosRecebidos = state.loans.reduce((sum, l) => {
                const totalComJuros = l.valor_parcela * l.prazo_meses;
                const juros = totalComJuros - l.valor_emprestimo;
                const pago = l.total_pago || 0;
                const proporcaoJuros = juros / totalComJuros;
                return sum + (pago * proporcaoJuros);
            }, 0);
            content += `Total Recebido: ${formatCurrency(totalRecebido)}\n`;
            content += `Juros Recebidos (estimado): ${formatCurrency(jurosRecebidos)}\n`;
            
        } else if (type === 'clients') {
            content += 'RELATÓRIO DE CLIENTES\n';
            content += '-'.repeat(40) + '\n\n';
            state.clients.forEach(client => {
                const clientLoans = state.loans.filter(l => l.cliente_id === client.id);
                const totalEmprestado = clientLoans.reduce((sum, l) => sum + l.valor_emprestimo, 0);
                const totalDevedor = clientLoans.reduce((sum, l) => sum + l.saldo_devedor, 0);
                content += `${client.nome}\n`;
                content += `  CPF/CNPJ: ${client.cpf_cnpj}\n`;
                content += `  Telefone: ${client.telefone}\n`;
                content += `  E-mail: ${client.email}\n`;
                content += `  Empréstimos: ${clientLoans.length}\n`;
                content += `  Total Emprestado: ${formatCurrency(totalEmprestado)}\n`;
                content += `  Saldo Devedor: ${formatCurrency(totalDevedor)}\n\n`;
            });
            
        } else if (type === 'monthly') {
            content += 'RELATÓRIO MENSAL\n';
            content += '-'.repeat(40) + '\n';
            content += 'Funcionalidade em desenvolvimento.\n';
        }
        
        // Ask where to save
        const result = await window.electronAPI.showSaveDialog({
            title: 'Salvar ' + reportName,
            defaultPath: `${reportName.replace(/\s+/g, '_')}_${hoje.toISOString().split('T')[0]}.txt`,
            filters: [
                { name: 'Arquivo de Texto', extensions: ['txt'] },
                { name: 'Todos os Arquivos', extensions: ['*'] }
            ]
        });
        
        if (!result.canceled && result.filePath) {
            const saveResult = await window.electronAPI.saveFile(result.filePath, content, 'utf8');
            if (saveResult.success) {
                showToast(`${reportName} salvo com sucesso!`, 'success');
            } else {
                showToast(`Erro ao salvar: ${saveResult.error}`, 'error');
            }
        }
        
    } catch (error) {
        showToast('Erro ao gerar relatório', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function exportData() {
    const exportIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>';
    
    const content = `
        <div class="export-options">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Escolha o formato de exportação:</h3>
            
            <div class="export-buttons" style="display: flex; flex-direction: column; gap: 1rem;">
                <button class="btn-export" onclick="exportToCSV('clients')" style="display: flex; align-items: center; gap: 0.75rem; padding: 1rem; border: 2px solid var(--border-color); border-radius: var(--radius); background: var(--bg-primary); cursor: pointer; transition: var(--transition);">
                    <span style="font-size: 1.5rem;">📊</span>
                    <div style="text-align: left;">
                        <strong style="color: var(--text-primary);">Clientes (CSV)</strong>
                        <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0;">Exportar lista de clientes para Excel</p>
                    </div>
                </button>
                
                <button class="btn-export" onclick="exportToCSV('loans')" style="display: flex; align-items: center; gap: 0.75rem; padding: 1rem; border: 2px solid var(--border-color); border-radius: var(--radius); background: var(--bg-primary); cursor: pointer; transition: var(--transition);">
                    <span style="font-size: 1.5rem;">💰</span>
                    <div style="text-align: left;">
                        <strong style="color: var(--text-primary);">Empréstimos (CSV)</strong>
                        <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0;">Exportar lista de empréstimos para Excel</p>
                    </div>
                </button>
                
                <button class="btn-export" onclick="exportToJSON()" style="display: flex; align-items: center; gap: 0.75rem; padding: 1rem; border: 2px solid var(--border-color); border-radius: var(--radius); background: var(--bg-primary); cursor: pointer; transition: var(--transition);">
                    <span style="font-size: 1.5rem;">📁</span>
                    <div style="text-align: left;">
                        <strong style="color: var(--text-primary);">Backup Completo (JSON)</strong>
                        <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0;">Exportar todos os dados para backup</p>
                    </div>
                </button>
            </div>
            
            <div class="modal-actions">
                <button type="button" class="btn-secondary" onclick="closeModal()">Fechar</button>
            </div>
        </div>
    `;
    
    openModal(`${exportIcon} Exportar Dados`, content);
}

async function exportToCSV(type) {
    closeModal();
    showLoading();
    
    try {
        let csvContent = '';
        let filename = '';
        const hoje = new Date().toISOString().split('T')[0];
        
        if (type === 'clients') {
            filename = `clientes_${hoje}.csv`;
            csvContent = 'Nome,CPF/CNPJ,Telefone,E-mail,Endereço\n';
            state.clients.forEach(c => {
                csvContent += `"${c.nome}","${c.cpf_cnpj}","${c.telefone}","${c.email}","${c.endereco || ''}"\n`;
            });
        } else if (type === 'loans') {
            filename = `emprestimos_${hoje}.csv`;
            csvContent = 'Cliente,Valor,Taxa Juros,Prazo,Parcela,Total Pago,Saldo Devedor,Data Empréstimo,Status\n';
            state.loans.forEach(l => {
                const client = state.clients.find(c => c.id === l.cliente_id);
                const status = calcularStatusEmprestimo(l);
                const clientName = client?.nome || 'N/A';
                csvContent += `"${clientName}","${l.valor_emprestimo}","${l.taxa_juros}%","${l.prazo_meses}","${l.valor_parcela}","${l.total_pago || 0}","${l.saldo_devedor}","${l.data_emprestimo}","${status.status}"\n`;
            });
        }
        
        const result = await window.electronAPI.showSaveDialog({
            title: 'Salvar CSV',
            defaultPath: filename,
            filters: [
                { name: 'CSV (Excel)', extensions: ['csv'] },
                { name: 'Todos os Arquivos', extensions: ['*'] }
            ]
        });
        
        if (!result.canceled && result.filePath) {
            // Add BOM for Excel UTF-8 compatibility
            const bom = '\uFEFF';
            const saveResult = await window.electronAPI.saveFile(result.filePath, bom + csvContent, 'utf8');
            if (saveResult.success) {
                showToast('Arquivo CSV exportado com sucesso!', 'success');
            } else {
                showToast(`Erro ao salvar: ${saveResult.error}`, 'error');
            }
        }
    } catch (error) {
        showToast('Erro ao exportar CSV', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function exportToJSON() {
    closeModal();
    showLoading();
    
    try {
        const hoje = new Date().toISOString().split('T')[0];
        const backup = {
            exportDate: new Date().toISOString(),
            version: '2.0.0',
            clients: state.clients,
            loans: state.loans
        };
        
        const result = await window.electronAPI.showSaveDialog({
            title: 'Salvar Backup',
            defaultPath: `financepro_backup_${hoje}.json`,
            filters: [
                { name: 'JSON', extensions: ['json'] },
                { name: 'Todos os Arquivos', extensions: ['*'] }
            ]
        });
        
        if (!result.canceled && result.filePath) {
            const content = JSON.stringify(backup, null, 2);
            const saveResult = await window.electronAPI.saveFile(result.filePath, content, 'utf8');
            if (saveResult.success) {
                showToast('Backup exportado com sucesso!', 'success');
            } else {
                showToast(`Erro ao salvar: ${saveResult.error}`, 'error');
            }
        }
    } catch (error) {
        showToast('Erro ao exportar backup', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

// Make functions available globally for onclick handlers
window.editClient = editClient;
window.viewClientLoans = viewClientLoans;
window.viewLoanDetails = viewLoanDetails;
window.openPaymentModal = openPaymentModal;
window.closeModal = closeModal;
window.generateReport = generateReport;
window.exportData = exportData;
window.exportToCSV = exportToCSV;
window.exportToJSON = exportToJSON;
window.createBackup = createBackup;
window.restoreBackup = restoreBackup;
