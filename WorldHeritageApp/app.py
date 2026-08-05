import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask, request
import logging
import db

APP = Flask(__name__)

@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) n_sites FROM Site)
    JOIN
      (SELECT COUNT(*) n_countries FROM Country)
    JOIN
      (SELECT COUNT(*) n_regions FROM Region)
    JOIN 
      (SELECT COUNT(*) n_categories FROM Category)
    JOIN 
      (SELECT COUNT(*) n_criteria FROM Criteria)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html', stats=stats)

@APP.route('/sites/')
def list_sites():
    sites = db.execute(
      '''
      SELECT 
        Site.id_no, 
        Site.name_en, 
        Site.date_inscribed, 
        Site.danger,
        Category.category_short,
        (SELECT GROUP_CONCAT(DISTINCT Country.name) 
         FROM Site_Country 
         JOIN Country ON CAST(Site_Country.iso_code AS TEXT) = Country.iso_code
         WHERE Site_Country.site_id = Site.id_no) as countries
      FROM Site
      LEFT JOIN Category ON Site.category_id = Category.category_id
      ORDER BY Site.id_no
      ''').fetchall()
    return render_template('site-list.html', sites=sites)

@APP.route('/sites/<int:id>/')
def get_site(id):
    site = db.execute(
      '''
      SELECT 
        Site.*, 
        Category.category, 
        Category.category_short,
        Site.short_description
      FROM Site
      LEFT JOIN Category ON Site.category_id = Category.category_id
      WHERE Site.id_no = ?
      ''', [id]).fetchone()

    countries = db.execute(
      '''
      SELECT Country.name, Country.iso_code
      FROM Site_Country
      JOIN Country ON CAST(Site_Country.iso_code AS TEXT) = Country.iso_code
      WHERE Site_Country.site_id = ?
      ORDER BY Country.name
      ''', [id]).fetchall()

    criteria = db.execute(
      '''
      SELECT Criteria.criteria_name, Criteria.criteria_description
      FROM Site_Criteria
      JOIN Criteria ON Site_Criteria.criteria_id = Criteria.criteria_id
      WHERE Site_Criteria.site_id = ?
      ORDER BY Criteria.criteria_id
      ''', [id]).fetchall()

    secondary_dates = db.execute(
      ''' 
      SELECT secondary_date
      FROM Site_Secondary_Dates
      WHERE site_id = ?
      ORDER BY secondary_date
      ''', [id]).fetchall()

    return render_template('site.html', 
             site=site, countries=countries, 
             criteria=criteria, secondary_dates=secondary_dates)

@APP.route('/sites/search/')
def search_site():
    expr = request.args.get('q', '')
    search = { 'expr': expr }
    
    if expr:
        expr = '%' + expr + '%'
        sites = db.execute(
            ''' 
            SELECT Site.id_no, Site.name_en, Site.date_inscribed
            FROM Site
            WHERE Site.name_en LIKE ?
            ORDER BY Site.id_no
            ''', [expr]).fetchall()
    else:
        sites = []
    
    return render_template('site-search.html', search=search, sites=sites)

@APP.route('/countries/')
def list_countries():
    countries_result = db.execute('''
      SELECT iso_code, name, region_id
      FROM Country
      ORDER BY name
    ''').fetchall()
    
    countries = []
    for row in countries_result:
        country = dict(row)
        region = db.execute(
            'SELECT name FROM Region WHERE region_id = ?',
            [country['region_id']]
        ).fetchone()
        country['region_name'] = region['name']
        countries.append(country)
    
    return render_template('country-list.html', countries=countries)

@APP.route('/countries/<string:iso_code>/')
def view_sites_by_country(iso_code):
    country = db.execute(
      '''
      SELECT Country.*, Region.name as region_name
      FROM Country
      LEFT JOIN Region ON Country.region_id = Region.region_id
      WHERE Country.iso_code = ?
      ''', [iso_code]).fetchone()

    sites = db.execute(
      '''
      SELECT 
        Site.id_no, 
        Site.name_en, 
        Site.date_inscribed, 
        Site.danger, 
        Category.category_short
      FROM Site
      JOIN Site_Country ON Site.id_no = Site_Country.site_id
      LEFT JOIN Category ON Site.category_id = Category.category_id
      WHERE CAST(Site_Country.iso_code AS TEXT) = ?
      ORDER BY Site.id_no
      ''', [iso_code]).fetchall()

    return render_template('country.html', country=country, sites=sites)

@APP.route('/countries/search/')
def search_country():
    expr = request.args.get('q', '')
    search = { 'expr': expr }
    
    if expr:
        expr = '%' + expr + '%'
        countries = db.execute(
            '''
            SELECT iso_code, name
            FROM Country
            WHERE name LIKE ?
            ORDER BY name
            ''', [expr]).fetchall()
    else:
        countries = []
    
    return render_template('country-search.html', search=search, countries=countries)

@APP.route('/regions/')
def list_regions():
    regions_result = db.execute('''
      SELECT region_id, name
      FROM Region
      ORDER BY region_id
    ''').fetchall()
    
    regions = []
    for row in regions_result:
        region = dict(row)
        count = db.execute(
            'SELECT COUNT(*) as count FROM Country WHERE region_id = ?',
            [region['region_id']]
        ).fetchone()
        region['country_count'] = count['count']
        regions.append(region)
    
    return render_template('region-list.html', regions=regions)

@APP.route('/regions/<int:id>/')
def view_countries_by_region(id):
    region = db.execute(
      '''
      SELECT region_id, name
      FROM Region
      WHERE region_id = ?
      ''', [id]).fetchone()

    countries = db.execute(
      '''
      SELECT iso_code, name
      FROM Country
      WHERE region_id = ?
      ORDER BY name
      ''', [id]).fetchall()

    return render_template('region.html', region=region, countries=countries)

@APP.route('/categories/')
def list_categories():
    categories = db.execute('''
      SELECT 
        Category.category_id, 
        Category.category, 
        Category.category_short,
        COUNT(Site.id_no) as site_count
      FROM Category
      LEFT JOIN Site ON Category.category_id = Site.category_id
      GROUP BY Category.category_id
      ORDER BY Category.category_id
    ''').fetchall()
    
    return render_template('category-list.html', categories=categories)

@APP.route('/categories/<int:id>/')
def view_sites_by_category(id):
    category = db.execute(
      '''
      SELECT category_id, category, category_short
      FROM Category
      WHERE category_id = ?
      ''', [id]).fetchone()

    sites = db.execute(
      '''
      SELECT Site.id_no, Site.name_en, Site.date_inscribed, Site.danger
      FROM Site
      WHERE Site.category_id = ?
      ORDER BY Site.id_no
      ''', [id]).fetchall()

    return render_template('category.html', category=category, sites=sites)

@APP.route('/criteria/')
def list_criteria():
    criteria = db.execute('''
      SELECT 
        Criteria.criteria_id, 
        Criteria.criteria_name, 
        Criteria.criteria_description,
        COUNT(DISTINCT Site_Criteria.site_id) as site_count
      FROM Criteria
      LEFT JOIN Site_Criteria ON Criteria.criteria_id = Site_Criteria.criteria_id
      GROUP BY Criteria.criteria_id
      ORDER BY Criteria.criteria_id
    ''').fetchall()
    
    return render_template('criteria-list.html', criteria=criteria)

@APP.route('/criteria/<int:id>/')
def view_sites_by_criteria(id):
    criterion = db.execute(
      '''
      SELECT criteria_id, criteria_name, criteria_description
      FROM Criteria
      WHERE criteria_id = ?
      ''', [id]).fetchone()

    sites = db.execute(
      '''
      SELECT DISTINCT Site.id_no, Site.name_en, Site.date_inscribed, Site.danger
      FROM Site
      JOIN Site_Criteria ON Site.id_no = Site_Criteria.site_id
      WHERE Site_Criteria.criteria_id = ?
      ORDER BY Site.id_no
      ''', [id]).fetchall()

    return render_template('criterion.html', criterion=criterion, sites=sites)

@APP.route('/danger/')
def list_danger_sites():
    sites = db.execute(
      '''
      SELECT 
        Site.id_no, 
        Site.name_en, 
        Site.date_inscribed, 
        Site.danger_list,
        (SELECT GROUP_CONCAT(DISTINCT Country.name) 
         FROM Site_Country 
         JOIN Country ON CAST(Site_Country.iso_code AS TEXT) = Country.iso_code
         WHERE Site_Country.site_id = Site.id_no) as countries
      FROM Site
      WHERE Site.danger = 1
      ORDER BY Site.id_no
      ''').fetchall()
    
    return render_template('danger-list.html', sites=sites)

@APP.route('/advanced-search/')
def advanced_search():
    country = request.args.get('country', '')
    region = request.args.get('region', '')
    category = request.args.get('category', '')
    criteria = request.args.get('criteria', '')
    danger = request.args.get('danger', '')
    
    query = '''
        SELECT DISTINCT 
          Site.id_no, 
          Site.name_en, 
          Site.date_inscribed, 
          Site.danger,
          GROUP_CONCAT(DISTINCT Country.name) as countries,
          Category.category_short
        FROM Site
        LEFT JOIN Category ON Site.category_id = Category.category_id
        LEFT JOIN Site_Country ON Site.id_no = Site_Country.site_id
        LEFT JOIN Country ON CAST(Site_Country.iso_code AS TEXT) = Country.iso_code
        LEFT JOIN Site_Criteria ON Site.id_no = Site_Criteria.site_id
        WHERE 1=1
    '''
    params = []
    
    if country:
        query += ' AND Country.iso_code = ?'
        params.append(country)
    
    if region:
        query += ' AND Country.region_id = ?'
        params.append(region)
    
    if category:
        query += ' AND Site.category_id = ?'
        params.append(category)
    
    if criteria:
        query += ' AND Site_Criteria.criteria_id = ?'
        params.append(criteria)
    
    if danger == 'yes':
        query += ' AND Site.danger = 1'
    elif danger == 'no':
        query += ' AND Site.danger = 0'
    
    query += ' GROUP BY Site.id_no ORDER BY Site.id_no'
    
    sites = db.execute(query, params).fetchall()
    
    countries = db.execute('SELECT iso_code, name FROM Country ORDER BY name').fetchall()
    regions = db.execute('SELECT region_id, name FROM Region ORDER BY region_id').fetchall()
    categories = db.execute('SELECT category_id, category FROM Category ORDER BY category_id').fetchall()
    criteria_list = db.execute('SELECT criteria_id, criteria_name FROM Criteria ORDER BY criteria_id').fetchall()
    
    return render_template('advanced-search.html', 
                          sites=sites,
                          countries=countries,
                          regions=regions,
                          categories=categories,
                          criteria_list=criteria_list,
                          filters=request.args)


# Query 1: Sítio com maior área
@APP.route('/query/1')
def query_1():
    result = db.execute('''
        SELECT 
            name_en AS "Local Mais Extenso", 
            area_hectares as "Área De Hectares"
        FROM 
            Site 
        WHERE area_hectares IS NOT NULL
        ORDER BY 
            area_hectares DESC 
        LIMIT 1
    ''').fetchone()
    return render_template('query-result.html', 
                          query_number=1,
                          result=result)

# Query 2: Países com mais de 5 sites
@APP.route('/query/2')
def query_2():
    result = db.execute('''
        SELECT 
            COUNT(T1.iso_code) AS "Número de Países Com Mais De 5 Sites" 
        FROM (
            SELECT 
                iso_code 
            FROM 
                Site_Country 
            GROUP BY 
                iso_code 
            HAVING 
                COUNT(site_id) > 5 
        ) AS T1
    ''').fetchone()
    return render_template('query-result.html',
                          query_number=2,
                          result=result)

# Query 3: Sites com latitude > 40 e longitude > 30
@APP.route('/query/3')
def query_3():
    results = db.execute('''
        SELECT 
            name_en AS "Nome Do Local", 
            latitude AS "Latitude", 
            longitude AS "Longitude"
        FROM 
            Site 
        WHERE 
            latitude > 40 
            AND longitude > 30
            AND latitude IS NOT NULL
            AND longitude IS NOT NULL
        ORDER BY name_en
    ''').fetchall()
    return render_template('query-results.html',
                          query_number=3,
                          results=results)

# Query 4: Critério mais aplicado
@APP.route('/query/4')
def query_4():
    result = db.execute('''
        SELECT 
            C.criteria_name AS "Criterio Mais Aplicado", 
            COUNT(SC.site_id) AS "Total Sites Aplicados" 
        FROM 
            Criteria C 
        JOIN 
            Site_Criteria SC ON C.criteria_id = SC.criteria_id 
        GROUP BY 
            C.criteria_name 
        ORDER BY 
            COUNT(SC.site_id) DESC 
        LIMIT 1
    ''').fetchone()
    return render_template('query-result.html',
                          query_number=4,
                          result=result)

# Query 5: Sites que não são da categoria "Cultural"
@APP.route('/query/5')
def query_5():
    results = db.execute('''

    SELECT 
        S.name_en AS "Nome Do Local",
        C.category AS "Categoria"
    FROM 
        Site S 
    JOIN 
        Category C ON S.category_id = C.category_id 
    WHERE 
        C.category = 'Natural' 
        AND C.category <> 'Mixed'
    ORDER BY
        S.name_en;
    ''').fetchall()
    return render_template('query-results.html',
                          query_number=5,
                          results=results)

# Query 6: Sites com "PARK" no nome
@APP.route('/query/6')
def query_6():
    results = db.execute('''
        SELECT 
            name_en AS "Nome Do Local"
        FROM 
            Site 
        WHERE 
            name_en LIKE '%PARK%'
        ORDER BY name_en
    ''').fetchall()
    return render_template('query-results.html',
                          query_number=6,
                          results=results)

# Query 7: Média de área por categoria
@APP.route('/query/7')
def query_7():
    results = db.execute('''
        SELECT 
            C.category AS "Nome Da Categoria", 
            ROUND(AVG(S.area_hectares), 2) AS "Média Da Área"
        FROM 
            Site S 
        JOIN 
            Category C ON S.category_id = C.category_id 
        WHERE S.area_hectares IS NOT NULL
        GROUP BY 
            C.category 
        ORDER BY 
            ROUND(AVG(S.area_hectares), 2) DESC
    ''').fetchall()
    return render_template('query-results.html',
                          query_number=7,
                          results=results)

# Query 8: Sites com justificação inscritos após 2010
@APP.route('/query/8')
def query_8():
    results = db.execute('''
        SELECT  
            name_en AS "Nome Do Local",  
            date_inscribed AS "Dados Inscritos",  
            justification AS "Justificação"
        FROM  
            Site 
        WHERE  
            justification IS NOT NULL 
            AND TRIM(justification) <> '' 
            AND CAST(date_inscribed AS INTEGER) > 2010 
        ORDER BY  
            CAST(date_inscribed AS INTEGER)
    ''').fetchall()
    return render_template('query-results.html',
                          query_number=8,
                          results=results)

# Query 9: Países sem sítios da categoria mais comum
@APP.route('/query/9')
def query_9():
    result = db.execute('''
        SELECT 
            COUNT(DISTINCT S.id_no) AS "Total de Sites Na Região 5"
        FROM 
            Site S
        JOIN 
            Site_Country SC ON S.id_no = SC.site_id
        JOIN 
            Country C ON SC.iso_code = C.iso_code
        JOIN 
            Region R ON C.region_id = R.region_id
        WHERE 
            R.region_id = 5
    ''').fetchone()
    return render_template('query-result.html',
                          query_number=9,
                          result=result)

# Query 10: Sites com descrição/justificação incompleta mas com mais de 4 critérios
@APP.route('/query/10')
def query_10():
    results = db.execute('''
        SELECT 
            S.name_en AS "Nome Do Local", 
            COUNT(SC.criteria_id) AS "Número Do Critério"
        FROM 
            Site S 
        JOIN 
            Site_Criteria SC ON S.id_no = SC.site_id 
        WHERE 
            (S.short_description IS NULL OR TRIM(S.short_description) = '') 
            OR (S.justification IS NULL OR TRIM(S.justification) = '') 
        GROUP BY 
            S.id_no, S.name_en 
        HAVING 
            COUNT(SC.criteria_id) > 4 
        ORDER BY 
            COUNT(SC.criteria_id) DESC
    ''').fetchall()
    return render_template('query-results.html',
                          query_number=10,
                          results=results)

# Query 11: Latitude média e posição relativa
@APP.route('/query/11')
def query_11():
    results = db.execute('''
        SELECT 
            S.name_en AS "Nome Do Local", 
            S.latitude AS "Latitude", 
            ROUND((S.latitude - Global_Avg.avg_latitude), 2) AS "Diferença Da Média", 
            CASE 
                WHEN S.latitude > Global_Avg.avg_latitude THEN 'Norte da Média' 
                WHEN S.latitude < Global_Avg.avg_latitude THEN 'Sul da Média' 
                ELSE 'Na Média' 
            END AS "Posição Relativa" 
        FROM 
            Site S 
        CROSS JOIN (
            SELECT 
                AVG(latitude) AS avg_latitude 
            FROM 
                Site 
            WHERE 
                latitude IS NOT NULL 
        ) AS Global_Avg 
        WHERE S.latitude IS NOT NULL
        ORDER BY 
            ROUND((S.latitude - Global_Avg.avg_latitude), 2) DESC
    ''').fetchall()
    return render_template('query-results.html',
                          query_number=11,
                          results=results)

# Query 12: Categoria com maior disparidade de área
@APP.route('/query/12')
def query_12():
    result = db.execute('''
        SELECT 
            C.category AS "Nome da Categoria", 
            SUM(S.area_hectares) AS "Área Total" 
        FROM 
            Category C 
        JOIN 
            Site S ON C.category_id = S.category_id 
        WHERE S.area_hectares IS NOT NULL
        GROUP BY 
            C.category_id, C.category
        LIMIT 1
    ''').fetchone()
    return render_template('query-result.html',
                          query_number=12,
                          result=result)

# Query 13: Sítios em perigo com data de fim expirada
@APP.route('/query/13')
def query_13():
    results = db.execute('''
        SELECT 
            name_en AS "Local Em Perigo Expirado", 
            date_end AS "Data Final", 
            date_inscribed AS "Data De Inscrição" 
        FROM 
            Site 
        WHERE 
            danger = 1 
            AND date_end IS NOT NULL
        ORDER BY date_end
    ''').fetchall()
    return render_template('query-results.html',
                          query_number=13,
                          results=results)


@APP.route('/queries/')
def list_queries():
    return render_template('queries.html')