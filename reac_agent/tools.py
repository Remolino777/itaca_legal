from langchain_core.tools import tool
import pandas as pd



@tool
def get_unique_categories() -> list:
    """
    Obtiene una lista de categorías únicas desde el archivo CSV.

    :return: Lista de categorías únicas o un mensaje de error.
    :rtype: list
    """
    try:
        #file_path = r'https://github.com/Remolino777/itaca_legal/blob/main/data/categorias_subcategorias.csv'
        file_path = path = 'categorias_subcategorias.csv'
        # Leer el archivo CSV con el encoding adecuado
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # Verificar si la columna 'Categoría' existe
        if "Categoría" not in df.columns:
            print("El archivo CSV no tiene una columna llamada 'Categoría'.")
            return []
        
        # Obtener valores únicos de la columna 'Categoría', eliminando nulos
        unique_categories = df["Categoría"].dropna().unique().tolist()
        
        # Verificar si se encontraron categorías
        if not unique_categories:
            print("No se encontraron categorías en el archivo CSV.")
            return []
        
        return unique_categories

    except FileNotFoundError:
        print("El archivo no se encontró.")
        return []
    except pd.errors.ParserError:
        print("Error al analizar el archivo CSV. Verifica el formato.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return []



@tool
def get_related_subcategories(categoria: str) -> list:
    """
    Obtiene las subcategorías relacionadas a una categoría específica.
    :param categoria: La categoría para la cual buscar subcategorías.
    :type categoria: str
    :return: Lista de subcategorías relacionadas a la categoría seleccionada.
    :rtype: list
    """
    
    
    # Normalizar el input: eliminar comillas, espacios extra y convertir a mayúsculas
    categoria_limpia = categoria.strip("'").strip().upper()   
    
    # Leer el CSV
    #path = r'https://github.com/Remolino777/itaca_legal/blob/main/data/categorias_subcategorias.csv'
    path = 'categorias_subcategorias.csv'
    try:
        df = pd.read_csv(path, encoding='utf-8')      
        
        # Normalizar las categorías del CSV
        df['Categoría'] = df['Categoría'].str.strip().str.upper()
        # Filtrar las subcategorías
        subcategorias_df = df[df['Categoría'] == categoria_limpia]
        
        if not subcategorias_df.empty:
            print(subcategorias_df)
        
        # Obtener la lista de subcategorías
        lista_subcategorias = subcategorias_df['Subcategoría'].tolist()
        if not lista_subcategorias:
            return f"No se encontraron subcategorías para la categoría '{categoria_limpia}'"
        return lista_subcategorias
    except Exception as e:
        return f"Error: {str(e)}"


    
   