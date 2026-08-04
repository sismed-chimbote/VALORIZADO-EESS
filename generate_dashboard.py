import json, base64, os

dir_path = r'C:\Users\PCSISMED\Desktop\DASHBOARD VALORIZADO POR EESS'

with open(os.path.join(dir_path, 'data.json'), encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False)

# Convertir imágenes a base64
with open(os.path.join(dir_path, 'SISMED.png'), 'rb') as f:
    b64_sismed = base64.b64encode(f.read()).decode('utf-8')

with open(os.path.join(dir_path, 'images.png'), 'rb') as f:
    b64_logo2 = base64.b64encode(f.read()).decode('utf-8')

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Ejecutivo - Valorizado por EESS y Microred</title>
    <!-- Google Fonts & Chart.js / XLSX / FontAwesome -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.08);
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.15);
            --secondary: #818cf8;
            --accent-green: #34d399;
            --accent-purple: #c084fc;
            --accent-amber: #fbbf24;
            --accent-rose: #fb7185;
            --accent-cyan: #22d3ee;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(129, 140, 248, 0.08) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
        }

        .main-container {
            flex: 1;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1.5rem;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.25rem 2rem;
        }

        .header-branding {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        }

        /* LOGOS ULTRA VISIBLES Y CON CONTRASTE */
        .logo-box {
            background: #ffffff;
            padding: 6px 14px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.2s ease;
        }

        .logo-box:hover {
            transform: scale(1.03);
        }

        .logo-img {
            height: 65px;
            width: auto;
            max-width: 180px;
            object-fit: contain;
            display: block;
        }

        .title-container h1 {
            font-size: 1.7rem;
            font-weight: 700;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .title-container p {
            color: var(--text-muted);
            font-size: 0.88rem;
            margin-top: 0.2rem;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .file-upload-btn {
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: var(--primary);
            padding: 0.7rem 1.3rem;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
        }

        .file-upload-btn:hover {
            background: rgba(56, 189, 248, 0.25);
            box-shadow: 0 0 15px var(--primary-glow);
        }

        /* Filtros */
        .filters-panel {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            display: flex;
            gap: 1.2rem;
            flex-wrap: wrap;
            align-items: center;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
            flex: 1;
            min-width: 180px;
        }

        .filter-group label {
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        select {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 0.65rem 0.9rem;
            border-radius: 8px;
            outline: none;
            font-size: 0.85rem;
            transition: border 0.3s;
        }

        select:focus {
            border-color: var(--primary);
        }

        /* Metrics Cards Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.5rem;
        }

        .kpi-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.25rem;
            position: relative;
            overflow: hidden;
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }

        .kpi-card.sis::before { background: var(--primary); }
        .kpi-card.intervencion::before { background: var(--accent-purple); }
        .kpi-card.ventas::before { background: var(--accent-green); }
        .kpi-card.exo::before { background: var(--accent-amber); }
        .kpi-card.soat::before { background: var(--accent-rose); }
        .kpi-card.dn::before { background: var(--accent-cyan); }

        .kpi-title {
            font-size: 0.78rem;
            color: var(--text-muted);
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .kpi-value {
            font-size: 1.4rem;
            font-weight: 700;
            margin: 0.4rem 0;
            color: var(--text-main);
        }

        .kpi-subtext {
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        /* Charts Grid - FIJADO CON ALTURA FIJA PARA EVITAR DISTORSIÓN EN ZOOM */
        .charts-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        @media (max-width: 1024px) {
            .charts-grid { grid-template-columns: 1fr; }
        }

        .chart-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
        }

        .chart-wrapper {
            position: relative;
            width: 100%;
            height: 320px; /* ALTURA FIJA PARA RESPOND DE CHART.JS */
        }

        .chart-header {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Table Card & Paginación */
        .table-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            overflow-x: auto;
            margin-bottom: 2rem;
        }

        .table-header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.85rem;
        }

        th {
            background: rgba(15, 23, 42, 0.5);
            padding: 0.8rem 0.8rem;
            color: var(--text-muted);
            font-weight: 600;
            border-bottom: 1px solid var(--card-border);
            white-space: nowrap;
        }

        td {
            padding: 0.75rem 0.8rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            white-space: nowrap;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }

        .badge {
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-eess {
            background: rgba(56, 189, 248, 0.1);
            color: var(--primary);
        }

        .badge-microred {
            background: rgba(192, 132, 252, 0.15);
            color: var(--accent-purple);
        }

        /* Controles de Paginación */
        .pagination-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1.25rem;
            flex-wrap: wrap;
            gap: 1rem;
            color: var(--text-muted);
            font-size: 0.85rem;
        }

        .pagination-controls {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .page-btn {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }

        .page-btn:hover:not(:disabled) {
            border-color: var(--primary);
            color: var(--primary);
        }

        .page-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .page-info {
            font-weight: 600;
            color: var(--text-main);
        }

        .page-size-selector {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .page-size-selector select {
            padding: 0.3rem 0.6rem;
            font-size: 0.8rem;
        }

        /* FOOTER DE COPYRIGHT MINIMALISTA DE AVENGINEERS Y AUTORÍA */
        .dashboard-footer {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: auto;
        }

        .footer-brand {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text-main);
            letter-spacing: 0.02em;
        }

        .footer-brand span {
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .footer-author {
            font-size: 0.78rem;
            color: #64748b; /* COLOR SUTIL Y MINIMALISTA QUE NO RESALTA EXCESIVAMENTE */
            font-weight: 400;
        }
    </style>
</head>
<body>

    <div class="main-container">
        <div class="header">
            <div class="header-branding">
                <div class="logo-box">
                    <img src="data:image/png;base64,__LOGO_SISMED__" alt="Logo SISMED" class="logo-img">
                </div>
                <div class="logo-box">
                    <img src="data:image/png;base64,__LOGO_2__" alt="Logo Institucional" class="logo-img">
                </div>
                <div class="title-container">
                    <h1><i class="fa-solid fa-chart-line"></i> Dashboard Ejecutivo Valorizado</h1>
                    <p>Monitoreo por Microred, EESS, Mes y Año con Paginación Completa de Registros</p>
                </div>
            </div>
            <div class="header-actions">
                <input type="file" id="excelFileInput" accept=".xlsx, .xls" style="display: none;">
                <button class="file-upload-btn" onclick="document.getElementById('excelFileInput').click()">
                    <i class="fa-solid fa-file-excel"></i> Cargar Otro Excel
                </button>
            </div>
        </div>

        <!-- Filtros -->
        <div class="filters-panel">
            <div class="filter-group">
                <label><i class="fa-solid fa-network-wired"></i> Microred</label>
                <select id="filterMicrored" onchange="onMicroredChange()">
                    <option value="ALL">Todas las Microredes</option>
                </select>
            </div>
            <div class="filter-group">
                <label><i class="fa-solid fa-hospital"></i> Establecimiento</label>
                <select id="filterEESS" onchange="applyFilters()">
                    <option value="ALL">Todos los Establecimientos</option>
                </select>
            </div>
            <div class="filter-group">
                <label><i class="fa-regular fa-calendar"></i> Año</label>
                <select id="filterAnio" onchange="applyFilters()">
                    <option value="ALL">Todos los Años</option>
                </select>
            </div>
            <div class="filter-group">
                <label><i class="fa-regular fa-calendar-days"></i> Mes</label>
                <select id="filterMes" onchange="applyFilters()">
                    <option value="ALL">Todos los Meses</option>
                </select>
            </div>
        </div>

        <!-- KPIs INDEPENDIENTES -->
        <div class="kpi-grid">
            <div class="kpi-card sis">
                <div class="kpi-title">VALORIZADO SIS <i class="fa-solid fa-hand-holding-medical"></i></div>
                <div class="kpi-value" id="kpiSIS">S/ 0.00</div>
                <div class="kpi-subtext" id="kpiRecetasSIS">0 Recetas SIS</div>
            </div>
            <div class="kpi-card intervencion">
                <div class="kpi-title">INTERVENCIÓN SANITARIA <i class="fa-solid fa-kit-medical"></i></div>
                <div class="kpi-value" id="kpiIntervencion">S/ 0.00</div>
                <div class="kpi-subtext" id="kpiRecetasIntervencion">0 Recetas Intervención</div>
            </div>
            <div class="kpi-card ventas">
                <div class="kpi-title">VENTAS DIRECTAS <i class="fa-solid fa-cash-register"></i></div>
                <div class="kpi-value" id="kpiVentas">S/ 0.00</div>
                <div class="kpi-subtext" id="kpiRecetasVentas">0 Recetas Ventas</div>
            </div>
            <div class="kpi-card exo">
                <div class="kpi-title">EXONERADOS <i class="fa-solid fa-heart-circle-check"></i></div>
                <div class="kpi-value" id="kpiExo">S/ 0.00</div>
                <div class="kpi-subtext" id="kpiRecetasExo">0 Recetas Exo.</div>
            </div>
            <div class="kpi-card soat">
                <div class="kpi-title">SOAT <i class="fa-solid fa-car-burst"></i></div>
                <div class="kpi-value" id="kpiSoat">S/ 0.00</div>
                <div class="kpi-subtext" id="kpiRecetasSoat">0 Recetas SOAT</div>
            </div>
            <div class="kpi-card dn">
                <div class="kpi-title">DEFENSA NACIONAL (DN) <i class="fa-solid fa-shield-halved"></i></div>
                <div class="kpi-value" id="kpiDN">S/ 0.00</div>
                <div class="kpi-subtext" id="kpiRecetasDN">0 Recetas DN</div>
            </div>
        </div>

        <!-- Gráficos -->
        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-header"><i class="fa-solid fa-chart-column"></i> Top 10 EESS por Componente Valorizado</div>
                <div class="chart-wrapper">
                    <canvas id="barChartEESS"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <div class="chart-header"><i class="fa-solid fa-chart-pie"></i> Proporción Independiente</div>
                <div class="chart-wrapper">
                    <canvas id="doughnutChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Tabla con Paginación -->
        <div class="table-card">
            <div class="table-header-container">
                <div class="chart-header" style="margin-bottom: 0;"><i class="fa-solid fa-table"></i> Detalle por Establecimiento, Microred y Periodo</div>
                <div class="page-size-selector">
                    <label style="font-size: 0.8rem; color: var(--text-muted);">Mostrar:</label>
                    <select id="pageSizeSelect" onchange="onPageSizeChange()">
                        <option value="15">15 registros</option>
                        <option value="25">25 registros</option>
                        <option value="50" selected>50 registros</option>
                        <option value="100">100 registros</option>
                        <option value="ALL">Todos los registros</option>
                    </select>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Microred</th>
                        <th>Establecimiento</th>
                        <th>Periodo</th>
                        <th>Valor SIS (S/)</th>
                        <th>Rec. SIS</th>
                        <th>Valor Intervención (S/)</th>
                        <th>Rec. Interv.</th>
                        <th>Valor Ventas (S/)</th>
                        <th>Rec. Ventas</th>
                        <th>Exonerados (S/)</th>
                        <th>Rec. Exo.</th>
                        <th>SOAT (S/)</th>
                        <th>Rec. SOAT</th>
                        <th>DN (S/)</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                </tbody>
            </table>

            <!-- Paginación -->
            <div class="pagination-container">
                <div id="paginationSummary">Mostrando 0 - 0 de 0 registros</div>
                <div class="pagination-controls">
                    <button class="page-btn" id="btnFirst" onclick="goToPage(1)"><i class="fa-solid fa-angles-left"></i></button>
                    <button class="page-btn" id="btnPrev" onclick="goToPage(currentPage - 1)"><i class="fa-solid fa-chevron-left"></i></button>
                    <span class="page-info">Página <span id="lblCurrentPage">1</span> de <span id="lblTotalPages">1</span></span>
                    <button class="page-btn" id="btnNext" onclick="goToPage(currentPage + 1)"><i class="fa-solid fa-chevron-right"></i></button>
                    <button class="page-btn" id="btnLast" onclick="goToPage(totalPages)"><i class="fa-solid fa-angles-right"></i></button>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER DE COPYRIGHT MINIMALISTA -->
    <footer class="dashboard-footer">
        <div class="footer-brand">
            <i class="fa-solid fa-shield-halved"></i> &copy; 2026 <span>AVengineers Agency</span>. Todos los derechos reservados.
        </div>
        <div class="footer-author">
            Desarrollado por Vasquez Carrillo Esteban
        </div>
    </footer>

    <script>
        let rawData = __DATA_JSON__;
        let currentFilteredData = [];
        let currentPage = 1;
        let pageSize = 50;
        let totalPages = 1;

        const mesNombres = {
            '01': 'Enero', '02': 'Febrero', '03': 'Marzo',
            '04': 'Abril', '05': 'Mayo', '06': 'Junio',
            '07': 'Julio', '08': 'Agosto', '09': 'Septiembre',
            '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
        };

        let chartBar = null;
        let chartDoughnut = null;

        function initDashboard() {
            populateFilterOptions();
            applyFilters();
        }

        function populateFilterOptions() {
            const microredes = new Set();
            const eessSet = new Set();
            const anios = new Set();
            const meses = new Set();

            rawData.forEach(item => {
                if (item.microred) microredes.add(item.microred);
                if (item.eess) eessSet.add(item.eess);
                if (item.periodo && String(item.periodo).length === 6) {
                    anios.add(String(item.periodo).substring(0, 4));
                    meses.add(String(item.periodo).substring(4, 6));
                }
            });

            // Microredes
            const selMicrored = document.getElementById('filterMicrored');
            selMicrored.innerHTML = '<option value="ALL">Todas las Microredes</option>';
            Array.from(microredes).sort().forEach(m => {
                selMicrored.innerHTML += `<option value="${m}">${m}</option>`;
            });

            // EESS
            updateEESSSelectOptions(Array.from(eessSet).sort());

            // Anio
            const selAnio = document.getElementById('filterAnio');
            selAnio.innerHTML = '<option value="ALL">Todos los Años</option>';
            Array.from(anios).sort().forEach(a => {
                selAnio.innerHTML += `<option value="${a}">${a}</option>`;
            });

            // Mes
            const selMes = document.getElementById('filterMes');
            selMes.innerHTML = '<option value="ALL">Todos los Meses</option>';
            Array.from(meses).sort().forEach(m => {
                selMes.innerHTML += `<option value="${m}">${mesNombres[m] || m}</option>`;
            });
        }

        function updateEESSSelectOptions(eessList) {
            const selEESS = document.getElementById('filterEESS');
            const currentVal = selEESS.value;
            selEESS.innerHTML = '<option value="ALL">Todos los Establecimientos</option>';
            eessList.forEach(e => {
                selEESS.innerHTML += `<option value="${e}">${e}</option>`;
            });
            if (eessList.includes(currentVal)) {
                selEESS.value = currentVal;
            } else {
                selEESS.value = 'ALL';
            }
        }

        function onMicroredChange() {
            const selMicrored = document.getElementById('filterMicrored').value;
            if (selMicrored === 'ALL') {
                const allEESS = new Set(rawData.map(r => r.eess));
                updateEESSSelectOptions(Array.from(allEESS).sort());
            } else {
                const filteredEESS = new Set(rawData.filter(r => r.microred === selMicrored).map(r => r.eess));
                updateEESSSelectOptions(Array.from(filteredEESS).sort());
            }
            applyFilters();
        }

        function applyFilters() {
            const selMicrored = document.getElementById('filterMicrored').value;
            const selEESS = document.getElementById('filterEESS').value;
            const selAnio = document.getElementById('filterAnio').value;
            const selMes = document.getElementById('filterMes').value;

            currentFilteredData = rawData.filter(item => {
                const p = String(item.periodo || '');
                const itemAnio = p.length === 6 ? p.substring(0, 4) : '';
                const itemMes = p.length === 6 ? p.substring(4, 6) : '';

                if (selMicrored !== 'ALL' && item.microred !== selMicrored) return false;
                if (selEESS !== 'ALL' && item.eess !== selEESS) return false;
                if (selAnio !== 'ALL' && itemAnio !== selAnio) return false;
                if (selMes !== 'ALL' && itemMes !== selMes) return false;
                return true;
            });

            updateKPIs(currentFilteredData);
            updateCharts(currentFilteredData);
            
            currentPage = 1;
            renderTablePage();
        }

        function updateKPIs(data) {
            let sis = 0, interv = 0, ventas = 0, exo = 0, soat = 0, dn = 0;
            let recSis = 0, recInterv = 0, recVentas = 0, recExo = 0, recSoat = 0, recDn = 0;

            data.forEach(item => {
                sis += item.sis || 0;
                interv += item.intervencion || 0;
                ventas += item.ventas || 0;
                exo += item.exo || 0;
                soat += item.soat || 0;
                dn += item.dn || 0;

                recSis += item.recetas_sis || 0;
                recInterv += item.recetas_intervencion || 0;
                recVentas += item.receta_ventas || 0;
                recExo += item.rec_exo || 0;
                recSoat += item.rec_soat || 0;
                recDn += item.rec_dn || 0;
            });

            document.getElementById('kpiSIS').innerText = 'S/ ' + sis.toLocaleString('es-PE', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            document.getElementById('kpiRecetasSIS').innerText = recSis.toLocaleString('es-PE') + ' Recetas SIS';

            document.getElementById('kpiIntervencion').innerText = 'S/ ' + interv.toLocaleString('es-PE', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            document.getElementById('kpiRecetasIntervencion').innerText = recInterv.toLocaleString('es-PE') + ' Recetas Interv.';

            document.getElementById('kpiVentas').innerText = 'S/ ' + ventas.toLocaleString('es-PE', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            document.getElementById('kpiRecetasVentas').innerText = recVentas.toLocaleString('es-PE') + ' Recetas Ventas';

            document.getElementById('kpiExo').innerText = 'S/ ' + exo.toLocaleString('es-PE', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            document.getElementById('kpiRecetasExo').innerText = recExo.toLocaleString('es-PE') + ' Recetas Exo.';

            document.getElementById('kpiSoat').innerText = 'S/ ' + soat.toLocaleString('es-PE', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            document.getElementById('kpiRecetasSoat').innerText = recSoat.toLocaleString('es-PE') + ' Recetas SOAT';

            document.getElementById('kpiDN').innerText = 'S/ ' + dn.toLocaleString('es-PE', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            document.getElementById('kpiRecetasDN').innerText = recDn.toLocaleString('es-PE') + ' Recetas DN';
        }

        function updateCharts(data) {
            const eessTotals = {};
            data.forEach(i => {
                const tot = (i.sis || 0) + (i.intervencion || 0) + (i.ventas || 0) + (i.exo || 0) + (i.soat || 0);
                eessTotals[i.eess] = (eessTotals[i.eess] || 0) + tot;
            });

            const sortedEESS = Object.entries(eessTotals)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);

            const topEESSList = sortedEESS.map(x => x[0]);
            
            const sisData = topEESSList.map(eess => data.filter(d => d.eess === eess).reduce((acc, curr) => acc + (curr.sis || 0), 0));
            const intervData = topEESSList.map(eess => data.filter(d => d.eess === eess).reduce((acc, curr) => acc + (curr.intervencion || 0), 0));
            const ventasData = topEESSList.map(eess => data.filter(d => d.eess === eess).reduce((acc, curr) => acc + (curr.ventas || 0), 0));

            if (chartBar) chartBar.destroy();
            const ctxBar = document.getElementById('barChartEESS').getContext('2d');
            chartBar = new Chart(ctxBar, {
                type: 'bar',
                data: {
                    labels: topEESSList,
                    datasets: [
                        { label: 'SIS', data: sisData, backgroundColor: '#38bdf8', borderRadius: 4 },
                        { label: 'Intervención', data: intervData, backgroundColor: '#c084fc', borderRadius: 4 },
                        { label: 'Ventas', data: ventasData, backgroundColor: '#34d399', borderRadius: 4 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false, // PREVIENE LA DISTORSIÓN EN ZOOM
                    plugins: { legend: { labels: { color: '#f8fafc' } } },
                    scales: {
                        y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                        x: { ticks: { color: '#94a3b8', font: { size: 9 } }, grid: { display: false } }
                    }
                }
            });

            let totalSIS = 0, totalInterv = 0, totalVentas = 0, totalExo = 0, totalSoat = 0;
            data.forEach(i => {
                totalSIS += i.sis || 0;
                totalInterv += i.intervencion || 0;
                totalVentas += i.ventas || 0;
                totalExo += i.exo || 0;
                totalSoat += i.soat || 0;
            });

            if (chartDoughnut) chartDoughnut.destroy();
            const ctxPie = document.getElementById('doughnutChart').getContext('2d');
            chartDoughnut = new Chart(ctxPie, {
                type: 'doughnut',
                data: {
                    labels: ['SIS', 'Intervención Sanitaria', 'Ventas Directas', 'Exonerados', 'SOAT'],
                    datasets: [{
                        data: [totalSIS, totalInterv, totalVentas, totalExo, totalSoat],
                        backgroundColor: ['#38bdf8', '#c084fc', '#34d399', '#fbbf24', '#fb7185']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false, // PREVIENE LA DISTORSIÓN EN ZOOM
                    plugins: {
                        legend: { position: 'bottom', labels: { color: '#f8fafc', font: { size: 11 } } }
                    }
                }
            });
        }

        // LÓGICA DE PAGINACIÓN DE LA TABLA
        function onPageSizeChange() {
            const val = document.getElementById('pageSizeSelect').value;
            pageSize = val === 'ALL' ? currentFilteredData.length : parseInt(val);
            currentPage = 1;
            renderTablePage();
        }

        function goToPage(page) {
            if (page < 1 || page > totalPages) return;
            currentPage = page;
            renderTablePage();
        }

        function renderTablePage() {
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            const total = currentFilteredData.length;
            if (total === 0) {
                tbody.innerHTML = '<tr><td colspan="14" style="text-align: center; color: var(--text-muted); padding: 2rem;">No se encontraron registros para los filtros seleccionados.</td></tr>';
                document.getElementById('paginationSummary').innerText = 'Mostrando 0 - 0 de 0 registros';
                document.getElementById('lblCurrentPage').innerText = '1';
                document.getElementById('lblTotalPages').innerText = '1';
                document.getElementById('btnFirst').disabled = true;
                document.getElementById('btnPrev').disabled = true;
                document.getElementById('btnNext').disabled = true;
                document.getElementById('btnLast').disabled = true;
                return;
            }

            const effectivePageSize = pageSize === 'ALL' ? total : pageSize;
            totalPages = Math.ceil(total / effectivePageSize);
            if (currentPage > totalPages) currentPage = totalPages;

            const startIdx = (currentPage - 1) * effectivePageSize;
            const endIdx = Math.min(startIdx + effectivePageSize, total);

            const pageData = currentFilteredData.slice(startIdx, endIdx);

            pageData.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><span class="badge badge-microred">${item.microred || 'N/A'}</span></td>
                    <td><span class="badge badge-eess">${item.eess}</span></td>
                    <td>${item.periodo}</td>
                    <td>S/ ${(item.sis || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</td>
                    <td>${item.recetas_sis || 0}</td>
                    <td>S/ ${(item.intervencion || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</td>
                    <td>${item.recetas_intervencion || 0}</td>
                    <td>S/ ${(item.ventas || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</td>
                    <td>${item.receta_ventas || 0}</td>
                    <td>S/ ${(item.exo || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</td>
                    <td>${item.rec_exo || 0}</td>
                    <td>S/ ${(item.soat || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</td>
                    <td>${item.rec_soat || 0}</td>
                    <td>S/ ${(item.dn || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</td>
                `;
                tbody.appendChild(row);
            });

            document.getElementById('paginationSummary').innerText = `Mostrando ${startIdx + 1} - ${endIdx} de ${total} registros`;
            document.getElementById('lblCurrentPage').innerText = currentPage;
            document.getElementById('lblTotalPages').innerText = totalPages;

            document.getElementById('btnFirst').disabled = currentPage === 1;
            document.getElementById('btnPrev').disabled = currentPage === 1;
            document.getElementById('btnNext').disabled = currentPage === totalPages;
            document.getElementById('btnLast').disabled = currentPage === totalPages;
        }

        // Helper para mapear columnas en Excel
        function getColValue(row, possibleNames) {
            const keys = Object.keys(row);
            for (let name of possibleNames) {
                const target = name.toLowerCase().replace(/\\s+/g, '');
                for (let k of keys) {
                    const cleanK = k.toLowerCase().replace(/\\s+/g, '');
                    if (cleanK === target) {
                        return row[k];
                    }
                }
            }
            return undefined;
        }

        // Excel Loader Flexible y Robusto con Microred
        document.getElementById('excelFileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(evt) {
                try {
                    const dataArr = new Uint8Array(evt.target.result);
                    const workbook = XLSX.read(dataArr, {type: 'array'});
                    const firstSheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[firstSheetName];
                    const json = XLSX.utils.sheet_to_json(worksheet);

                    if (!json || json.length === 0) {
                        alert('El archivo Excel seleccionado parece estar vacío o no contiene datos válidos.');
                        return;
                    }

                    rawData = json.map(r => {
                        const eessVal = getColValue(r, ['establecimiento', 'eess', 'nom_eess', 'nombre']) || '';
                        const microredVal = getColValue(r, ['microred', 'micro_red', 'micro red', 'red']) || '';
                        const periodoVal = getColValue(r, ['aÃ±o mes', 'año mes', 'periodo', 'ao mes', 'a?o mes', 'anomes']) || '';
                        
                        return {
                            eess: String(eessVal).trim(),
                            microred: String(microredVal).trim(),
                            periodo: String(periodoVal).trim(),
                            receta_ventas: parseFloat(getColValue(r, ['receta ventas', 'receta_ventas', 'rec_ventas']) || 0),
                            recetas_sis: parseFloat(getColValue(r, ['recetas sis', 'recetas_sis', 'rec_sis']) || 0),
                            recetas_intervencion: parseFloat(getColValue(r, ['recetas intervencion', 'recetas intervencion ', 'recetas_intervencion', 'rec_intervencion']) || 0),
                            rec_exo: parseFloat(getColValue(r, ['rec_exo', 'recetas exo', 'recetas exonerados']) || 0),
                            rec_soat: parseFloat(getColValue(r, ['rec_soat', 'recetas soat']) || 0),
                            rec_dn: parseFloat(getColValue(r, ['rec_dn', 'recetas dn']) || 0),
                            ventas: parseFloat(getColValue(r, ['ventas', 'monto_ventas']) || 0),
                            sis: parseFloat(getColValue(r, ['sis', 'monto_sis']) || 0),
                            intervencion: parseFloat(getColValue(r, ['intervencion sanitaria', 'intervencion_sanitaria', 'intervencion', 'monto_intervencion']) || 0),
                            exo: parseFloat(getColValue(r, ['exo', 'exonerado', 'exonerados']) || 0),
                            soat: parseFloat(getColValue(r, ['soat', 'monto_soat']) || 0),
                            dn: parseFloat(getColValue(r, ['dn', 'defensa_nacional']) || 0)
                        };
                    });

                    initDashboard();
                    alert(`¡Excel cargado con éxito! Se procesaron ${rawData.length} registros.`);
                } catch (err) {
                    console.error("Error al procesar Excel:", err);
                    alert('Ocurrió un error al leer el archivo Excel. Asegúrate de seleccionar una plantilla compatible de SISMED.');
                }
            };
            reader.readAsArrayBuffer(file);
        });

        // Garantiza re-render de gráficos al redimensionar pantalla/zoom
        window.onresize = function() {
            if (currentFilteredData && currentFilteredData.length > 0) {
                updateCharts(currentFilteredData);
            }
        };

        window.onload = initDashboard;
    </script>
</body>
</html>
"""

html_final = html_template.replace('__DATA_JSON__', json_str).replace('__LOGO_SISMED__', b64_sismed).replace('__LOGO_2__', b64_logo2)

with open(os.path.join(dir_path, 'dashboard.html'), 'w', encoding='utf-8') as out_f:
    out_f.write(html_final)

print("PIE DE PÁGINA MINIMALISTA ACTUALIZADO CON ÉXITO")
