from Utils.tools import Tools, CustomException
from Utils.querys import Querys
import pandas as pd
import base64
from io import BytesIO
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

class Descripcion:
    """
    Clase para gestionar la lógica de negocio de años y objetivos del plan de ventas.
    """

    def __init__(self, db):
        self.db = db
        self.tools = Tools()
        self.querys = Querys(self.db)

    # Función para buscar por número de pedido
    def buscar_por_numero(self, numero: str):
        """
        Busca documentos por número de pedido en dos tablas diferentes.
        
        Args:
            numero (str): Número de pedido a buscar
        """
        try:
            if not numero:
                raise CustomException("El número de pedido es requerido")

            # Ejecutar consultas usando querys
            result1 = self.querys.buscar_documentos_actuales(numero)
            result2 = self.querys.buscar_documentos_historia(numero)
            
            # Convertir resultados a lista de diccionarios
            documentos_actuales = [
                {
                    "codigo": row[0],
                    "valor_unitario": float(row[1]) if row[1] is not None else 0,
                    "descripcion2": row[2]
                }
                for row in result1
            ]
            
            documentos_historia = [
                {
                    "codigo": row[0],
                    "valor_unitario": float(row[1]) if row[1] is not None else 0,
                    "descripcion2": row[2]
                }
                for row in result2
            ]
            
            return self.tools.output(
                200, 
                f"Búsqueda exitosa para el pedido {numero}",
                {
                    "documentos_actuales": documentos_actuales,
                    "documentos_historia": documentos_historia,
                    "total_actuales": len(documentos_actuales),
                    "total_historia": len(documentos_historia)
                }
            )
            
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Error al buscar por número: {e}")
            raise CustomException(f"Error al buscar por número: {str(e)}")

    # Función para actualizar descripciones de documentos
    def actualizar_descripciones(self, data: dict):
        """
        Actualiza las descripciones de múltiples documentos.
        
        Args:
            data (dict): {"numero": "12345", "descripciones": [{"codigo": "ABC", "valor_unitario": 100, "descripcion2": "..."}]}
        """
        try:
            numero = data.get("numero")
            descripciones = data.get("descripciones", [])

            if not numero:
                raise CustomException("El número de pedido es requerido")
            
            if not descripciones or len(descripciones) == 0:
                raise CustomException("No hay descripciones para actualizar")

            actualizados = 0
            errores = []

            # Actualizar cada descripción
            for desc in descripciones:
                codigo = desc.get("codigo")
                valor_unitario = desc.get("valor_unitario")
                descripcion2 = desc.get("descripcion2")

                if not codigo or descripcion2 is None:
                    continue

                try:
                    rows = self.querys.actualizar_descripcion_documento(
                        numero, 
                        codigo, 
                        valor_unitario, 
                        descripcion2
                    )
                    actualizados += rows
                except Exception as e:
                    errores.append(f"Error al actualizar {codigo}: {str(e)}")

            mensaje = f"Se actualizaron {actualizados} descripción(es) exitosamente"
            if errores:
                mensaje += f". Errores: {', '.join(errores)}"
            
            return self.tools.output(
                200, 
                mensaje,
                {
                    "actualizados": actualizados,
                    "total_enviados": len(descripciones),
                    "errores": errores
                }
            )
            
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Error al actualizar descripciones: {e}")
            raise CustomException(f"Error al actualizar descripciones: {str(e)}")
