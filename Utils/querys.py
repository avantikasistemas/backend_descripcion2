from Utils.tools import Tools, CustomException
from sqlalchemy import text, func, select, and_
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime
from collections import defaultdict
from typing import List, Dict, Any
import json

class Querys:

    def __init__(self, db):
        self.db = db
        self.tools = Tools()
        self.query_params = dict()

    # Query para obtener últimos datos procesados activos
    def obtener_ultimos_datos_procesados(self):
        """
        Obtiene los últimos registros activos de tipo 1 (DIAN) y tipo 2 (DMS).
        
        Returns:
            dict: {"dian": {...}, "dms": {...}}
        """
        try:
            # Obtener último registro DIAN (tipo=1) activo
            query_dian = text("""
                SELECT TOP 1 id, tipo, datos, fecha_creacion
                FROM dbo.intranet_contabilidad_datos_depuracion
                WHERE tipo = 1 AND estado = 1
                ORDER BY fecha_creacion DESC
            """)
            
            resultado_dian = self.db.execute(query_dian).fetchone()
            
            # Obtener último registro DMS (tipo=2) activo
            query_dms = text("""
                SELECT TOP 1 id, tipo, datos, fecha_creacion
                FROM dbo.intranet_contabilidad_datos_depuracion
                WHERE tipo = 2 AND estado = 1
                ORDER BY fecha_creacion DESC
            """)
            
            resultado_dms = self.db.execute(query_dms).fetchone()
            
            datos = {
                "dian": None,
                "dms": None
            }
            
            if resultado_dian:
                datos["dian"] = {
                    "id": resultado_dian[0],
                    "tipo": resultado_dian[1],
                    "datos": json.loads(resultado_dian[2]),
                    "fecha_creacion": resultado_dian[3].isoformat() if resultado_dian[3] else None
                }
            
            if resultado_dms:
                datos["dms"] = {
                    "id": resultado_dms[0],
                    "tipo": resultado_dms[1],
                    "datos": json.loads(resultado_dms[2]),
                    "fecha_creacion": resultado_dms[3].isoformat() if resultado_dms[3] else None
                }
            
            return datos
            
        except Exception as e:
            raise CustomException(f"Error al obtener últimos datos procesados: {str(e)}")

    # Query para buscar documentos actuales por número de pedido
    def buscar_documentos_actuales(self, numero: str):
        """
        Busca documentos actuales por número de pedido.
        
        Args:
            numero (str): Número de pedido
            
        Returns:
            list: Lista de documentos encontrados
        """
        try:
            query = text("""
                SELECT codigo, valor_unitario, descripcion2, cantidad
                FROM documentos_lin_ped 
                WHERE numero = :numero AND sw = 1 AND descripcion2 IS NULL 
                ORDER BY codigo ASC
            """)
            
            result = self.db.execute(query, {"numero": numero}).fetchall()
            return result
            
        except Exception as e:
            raise CustomException(f"Error al buscar documentos actuales: {str(e)}")

    # Query para buscar documentos históricos por número de pedido
    def buscar_documentos_historia(self, numero: str):
        """
        Busca documentos históricos por número de pedido.
        
        Args:
            numero (str): Número de pedido
            
        Returns:
            list: Lista de documentos históricos encontrados
        """
        try:
            query = text("""
                SELECT codigo, valor_unitario, descripcion2, cantidad 
                FROM documentos_lin_ped_historia 
                WHERE numero = :numero AND sw = 1 
                ORDER BY codigo ASC
            """)
            
            result = self.db.execute(query, {"numero": numero}).fetchall()
            return result
            
        except Exception as e:
            raise CustomException(f"Error al buscar documentos históricos: {str(e)}")

    # Query para actualizar descripción de un documento
    def actualizar_descripcion_documento(self, numero: str, codigo: str, valor_unitario: float, cantidad: float, descripcion2: str):
        """
        Actualiza la descripción2 de un documento específico.
        
        Args:
            numero (str): Número de pedido
            codigo (str): Código del producto
            valor_unitario (float): Valor unitario del producto
            cantidad (float): Cantidad del producto
            descripcion2 (str): Nueva descripción
            
        Returns:
            int: Número de filas afectadas
        """
        try:
            query = text("""
                UPDATE documentos_lin_ped 
                SET descripcion2 = :descripcion2 
                WHERE numero = :numero 
                AND sw = 1 
                AND codigo = :codigo 
                AND valor_unitario = :valor_unitario
                AND cantidad = :cantidad
            """)
            
            result = self.db.execute(query, {
                "descripcion2": descripcion2,
                "numero": numero,
                "codigo": codigo,
                "valor_unitario": valor_unitario,
                "cantidad": cantidad
            })
            
            self.db.commit()
            return result.rowcount
            
        except Exception as e:
            self.db.rollback()
            raise CustomException(f"Error al actualizar descripción: {str(e)}")
