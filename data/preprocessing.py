import polars as pl
from os import path

def csv(file):
    return path.join('data','contents',file)

def population_world():
    return(
        pl.read_csv(csv('pop.csv'), separator=',', null_values='')
        .unpivot(on=['1800','1801','1802','1803','1804','1805','1806','1807','1808','1809','1810','1811','1812','1813','1814','1815','1816','1817','1818','1819','1820','1821','1822','1823','1824','1825','1826','1827','1828','1829','1830','1831','1832','1833','1834','1835','1836','1837','1838','1839','1840','1841','1842','1843','1844','1845','1846','1847','1848','1849','1850','1851','1852','1853','1854','1855','1856','1857','1858','1859','1860','1861','1862','1863','1864','1865','1866','1867','1868','1869','1870','1871','1872','1873','1874','1875','1876','1877','1878','1879','1880','1881','1882','1883','1884','1885','1886','1887','1888','1889','1890','1891','1892','1893','1894','1895','1896','1897','1898','1899','1900','1901','1902','1903','1904','1905','1906','1907','1908','1909','1910','1911','1912','1913','1914','1915','1916','1917','1918','1919','1920','1921','1922','1923','1924','1925','1926','1927','1928','1929','1930','1931','1932','1933','1934','1935','1936','1937','1938','1939','1940','1941','1942','1943','1944','1945','1946','1947','1948','1949','1950','1951','1952','1953','1954','1955','1956','1957','1958','1959','1960','1961','1962','1963','1964','1965','1966','1967','1968','1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030','2031','2032','2033','2034','2035','2036','2037','2038','2039','2040','2041','2042','2043','2044','2045','2046','2047','2048','2049','2050','2051','2052','2053','2054','2055','2056','2057','2058','2059','2060','2061','2062','2063','2064','2065','2066','2067','2068','2069','2070','2071','2072','2073','2074','2075','2076','2077','2078','2079','2080','2081','2082','2083','2084','2085','2086','2087','2088','2089','2090','2091','2092','2093','2094','2095','2096','2097','2098','2099','2100'],
                 index='country',
                 variable_name='Year',
                 value_name='Population')
        .select(
            pl.col('country').str.replace('USA', 'United States')
                             .str.replace('UK', 'United Kingdom'),
            pl.col('Year').cast(pl.Int16),
            pl.col('Population').str.replace('k$','e3')
                                .str.replace('M$','e6')
                                .str.replace('B$','e9')
                                .cast(pl.Float64)
        )
        .filter(pl.col('Year') > 1949)
        .filter(pl.col('Year') < 2022)
        .rename({'country':'Country/area'})
    )

def veg_consumption( ):
    # Data sources: Food and Agriculture Organization of the United Nations (2023)Food and Agriculture Organization of the United Nations (2023) – with major processing by Our World in Data
    return(
        pl.read_csv(csv('vegetable-consumption-per-capita.csv'), separator=',', null_values='')
        .rename(
            {'Vegetables | 00002918 || Food available for consumption | 0645pc || kilograms per year per capita':'Vegetables consumption',
             'Entity':'Country/area'}
        )
    )

def life_exp_world():
    return(
        pl.read_csv(csv('life-expectancy-hmd-unwpp.csv'), separator=',', null_values='')
        .rename(
            {'Life expectancy - Sex: total - Age: 0 - Type: period':'Life expectancy',
             'Entity':'Country/area'}
        )
    )

obesity = (
    pl.read_csv(csv('share-of-adults-defined-as-obese.csv'), separator=',', null_values='')
    .rename(
        {'Entity':'Country/area',
            'Prevalence of obesity among adults, BMI >= 30 (crude estimate) (%) - Sex: both sexes - Age group: 18+  years':'Obesity'}
    )
)

def veg_vs_lifeexp():
    return(
        veg_consumption()
        .join(life_exp_world(), on=['Country/area','Code','Year'], how='inner')
        .join(population_world(), on=['Country/area','Year'])
        .join(obesity, on=['Code','Country/area','Year'])
    )

diet2 = (
    pl.read_csv(csv('dietary-composition-by-country.csv'), separator=',', null_values='')
    .rename({'Entity':'Country/area'})
    .unpivot(
        on=['Miscellaneous group | 00002928 || Food available for consumption | 0664pc || kilocalories per day per capita','Alcoholic Beverages | 00002924 || Food available for consumption | 0664pc || kilocalories per day per capita','Animal fats group | 00002946 || Food available for consumption | 0664pc || kilocalories per day per capita','Vegetable Oils | 00002914 || Food available for consumption | 0664pc || kilocalories per day per capita','Oilcrops | 00002913 || Food available for consumption | 0664pc || kilocalories per day per capita','Fish and seafood | 00002960 || Food available for consumption | 0664pc || kilocalories per day per capita','Sugar crops | 00002908 || Food available for consumption | 0664pc || kilocalories per day per capita','Sugar & Sweeteners | 00002909 || Food available for consumption | 0664pc || kilocalories per day per capita','Starchy Roots | 00002907 || Food available for consumption | 0664pc || kilocalories per day per capita',"Meat, Other | 00002735 || Food available for consumption | 0664pc || kilocalories per day per capita","Meat, sheep and goat | 00002732 || Food available for consumption | 0664pc || kilocalories per day per capita","Meat, pig | 00002733 || Food available for consumption | 0664pc || kilocalories per day per capita","Meat, poultry | 00002734 || Food available for consumption | 0664pc || kilocalories per day per capita","Meat, beef | 00002731 || Food available for consumption | 0664pc || kilocalories per day per capita",'Eggs | 00002949 || Food available for consumption | 0664pc || kilocalories per day per capita','Milk | 00002948 || Food available for consumption | 0664pc || kilocalories per day per capita','Nuts | 00002551 || Food available for consumption | 0664pc || kilocalories per day per capita','Fruit | 00002919 || Food available for consumption | 0664pc || kilocalories per day per capita','Vegetables | 00002918 || Food available for consumption | 0664pc || kilocalories per day per capita','Pulses | 00002911 || Food available for consumption | 0664pc || kilocalories per day per capita',"Cereals, Other | 00002520 || Food available for consumption | 0664pc || kilocalories per day per capita",'Barley | 00002513 || Food available for consumption | 0664pc || kilocalories per day per capita','Maize | 00002514 || Food available for consumption | 0664pc || kilocalories per day per capita','Rice | 00002807 || Food available for consumption | 0664pc || kilocalories per day per capita','Wheat | 00002511 || Food available for consumption | 0664pc || kilocalories per day per capita'],
        index=['Country/area','Year'],
        variable_name='Food type',
        value_name='Food available for consumption'
    )
    .with_columns(
        pl.col('Food type').str.replace(r' \|.+kilocalories per day per capita$','')
    )
)

# for testing
if __name__=='__main__':
    print(diet2)