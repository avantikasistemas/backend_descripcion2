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

    # Query para buscar documentos actuales por número de pedido
    def buscar_documentos_actuales(self, numero: str):
        """
        Busca documentos actuales por número de pedido.
        
        Args:
            numero (str): Número de pedido
            
        Returns:
            list: Lista de diccionarios con los documentos encontrados
        """
        try:
            query = text("""
                SELECT seq, codigo, valor_unitario, descripcion2, cantidad
                FROM documentos_lin_ped 
                WHERE numero = :numero AND sw = 1 AND descripcion2 IS NULL 
                ORDER BY codigo ASC
            """)
            
            result = self.db.execute(query, {"numero": numero}).fetchall()
            
            # Convertir a lista de diccionarios
            documentos = [
                {
                    "seq": int(row.seq) if row.seq is not None else 0,
                    "codigo": row.codigo,
                    "valor_unitario": float(row.valor_unitario) if row.valor_unitario is not None else 0,
                    "descripcion2": row.descripcion2,
                    "cantidad": float(row.cantidad) if row.cantidad is not None else 0
                }
                for row in result
            ]
            
            return documentos
            
        except Exception as e:
            raise CustomException(f"Error al buscar documentos actuales: {str(e)}")

    # Query para buscar documentos históricos por número de pedido
    def buscar_documentos_historia(self, numero: str):
        """
        Busca documentos históricos por número de pedido.
        
        Args:
            numero (str): Número de pedido
            
        Returns:
            list: Lista de diccionarios con los documentos históricos encontrados
        """
        try:
            query = text("""
                SELECT seq, codigo, valor_unitario, descripcion2, cantidad 
                FROM documentos_lin_ped_historia 
                WHERE numero = :numero AND sw = 1 
                ORDER BY codigo ASC
            """)
            
            result = self.db.execute(query, {"numero": numero}).fetchall()
            
            # Convertir a lista de diccionarios
            documentos = [
                {
                    "seq": int(row.seq) if row.seq is not None else 0,
                    "codigo": row.codigo,
                    "valor_unitario": float(row.valor_unitario) if row.valor_unitario is not None else 0,
                    "descripcion2": row.descripcion2,
                    "cantidad": float(row.cantidad) if row.cantidad is not None else 0
                }
                for row in result
            ]
            
            return documentos
            
        except Exception as e:
            raise CustomException(f"Error al buscar documentos históricos: {str(e)}")

    # Query para actualizar descripción de un documento
    def actualizar_descripcion_documento(self, numero: str, seq: int, codigo: str, valor_unitario: float, cantidad: float, descripcion2: str):
        """
        Actualiza la descripción2 de un documento específico.
        
        Args:
            numero (str): Número de pedido
            seq (int): Secuencia del documento
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
                AND seq = :seq
                AND codigo = :codigo 
                AND valor_unitario = :valor_unitario
                AND cantidad = :cantidad
            """)
            
            result = self.db.execute(query, {
                "descripcion2": descripcion2,
                "numero": numero,
                "seq": seq,
                "codigo": codigo,
                "valor_unitario": valor_unitario,
                "cantidad": cantidad
            })
            
            self.db.commit()
            return result.rowcount
            
        except Exception as e:
            self.db.rollback()
            raise CustomException(f"Error al actualizar descripción: {str(e)}")
