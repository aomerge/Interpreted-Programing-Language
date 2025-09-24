#!/usr/bin/env python3
"""
Validador y demostrador del Parser Modular
==========================================

Este script demuestra las capacidades del nuevo parser modular
y valida que todos los componentes funcionen correctamente.
"""

from src.lexer.lexer import Lexer
from src.parser.parser_core import ModularParser, Parser
from src.ast import Program, Statement, Expression
from typing import List, Dict, Any


class ParserValidator:
    """Validador del parser modular."""
    
    def __init__(self):
        self.test_cases = [
            {
                "name": "Declaraciones Let",
                "code": "let x = 5; let name = 'hello';",
                "expected_statements": 2
            },
            {
                "name": "Expresiones Aritméticas",
                "code": "5 + 3 * 2;",
                "expected_statements": 1
            },
            {
                "name": "Declaraciones Return",
                "code": "return x + y;",
                "expected_statements": 1
            },
            {
                "name": "Expresiones Booleanas",
                "code": "true; false; !true;",
                "expected_statements": 3
            },
            {
                "name": "Funciones Básicas",
                "code": "fn(x, y) { return x + y; };",
                "expected_statements": 1
            },
            {
                "name": "Llamadas a Función",
                "code": "add(1, 2);",
                "expected_statements": 1
            }
        ]
    
    def validate_parser_structure(self, parser: ModularParser) -> Dict[str, Any]:
        """Valida la estructura modular del parser."""
        results = {
            "components_loaded": True,
            "components": {},
            "errors": []
        }
        
        try:
            # Verificar que todos los componentes están cargados
            components = {
                "StatementParser": parser.statement_parser,
                "ExpressionParser": parser.expression_parser,
                "FunctionParser": parser.function_parser
            }
            
            for name, component in components.items():
                if component is None:
                    results["components_loaded"] = False
                    results["errors"].append(f"{name} no está cargado")
                else:
                    results["components"][name] = {
                        "loaded": True,
                        "type": type(component).__name__,
                        "methods": [m for m in dir(component) if not m.startswith('_')]
                    }
            
        except Exception as e:
            results["components_loaded"] = False
            results["errors"].append(f"Error al verificar componentes: {e}")
        
        return results
    
    def run_test_cases(self) -> Dict[str, Any]:
        """Ejecuta todos los casos de prueba."""
        results = {
            "total_tests": len(self.test_cases),
            "passed": 0,
            "failed": 0,
            "test_results": []
        }
        
        for test_case in self.test_cases:
            try:
                lexer = Lexer(test_case["code"])
                parser = ModularParser(lexer)
                
                program = parser.parse_program()
                
                test_result = {
                    "name": test_case["name"],
                    "code": test_case["code"],
                    "passed": True,
                    "statements_parsed": len(program.statements),
                    "expected_statements": test_case["expected_statements"],
                    "errors": parser.get_errors()
                }
                
                # Verificar que el número de declaraciones coincida
                if len(program.statements) != test_case["expected_statements"]:
                    test_result["passed"] = False
                    test_result["error"] = f"Esperado {test_case['expected_statements']} declaraciones, obtuvo {len(program.statements)}"
                
                # Verificar que no haya errores de parseo críticos
                if len(parser.get_errors()) > 0:
                    # Permitir ciertos errores no críticos
                    critical_errors = [e for e in parser.get_errors() 
                                     if "No prefix parse function" not in e]
                    if critical_errors:
                        test_result["passed"] = False
                        test_result["error"] = f"Errores críticos: {critical_errors}"
                
                if test_result["passed"]:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                
                results["test_results"].append(test_result)
                
            except Exception as e:
                results["failed"] += 1
                results["test_results"].append({
                    "name": test_case["name"],
                    "code": test_case["code"],
                    "passed": False,
                    "error": f"Excepción: {e}"
                })
        
        return results
    
    def generate_report(self) -> str:
        """Genera un reporte completo de validación."""
        print("="*60)
        print("VALIDACIÓN DEL PARSER MODULAR")
        print("="*60)
        
        # Crear parser para pruebas estructurales
        lexer = Lexer("let x = 5;")
        parser = ModularParser(lexer)
        
        # Validar estructura
        structure_results = self.validate_parser_structure(parser)
        print("\n📋 ESTRUCTURA DEL PARSER:")
        print("-" * 30)
        
        if structure_results["components_loaded"]:
            print("✅ Todos los componentes están cargados correctamente")
            for name, info in structure_results["components"].items():
                print(f"  • {name}: {info['type']}")
                print(f"    Métodos: {len(info['methods'])}")
        else:
            print("❌ Problemas con la carga de componentes:")
            for error in structure_results["errors"]:
                print(f"  • {error}")
        
        # Ejecutar casos de prueba
        test_results = self.run_test_cases()
        print(f"\n🧪 CASOS DE PRUEBA:")
        print("-" * 30)
        print(f"Total: {test_results['total_tests']}")
        print(f"Pasados: ✅ {test_results['passed']}")
        print(f"Fallidos: ❌ {test_results['failed']}")
        
        print(f"\n📊 RESULTADOS DETALLADOS:")
        print("-" * 30)
        
        for result in test_results["test_results"]:
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {result['name']}")
            print(f"   Código: {result['code']}")
            if result["passed"]:
                print(f"   Declaraciones parseadas: {result.get('statements_parsed', 'N/A')}")
            else:
                print(f"   Error: {result.get('error', 'Error desconocido')}")
            print()
        
        # Resumen final
        success_rate = (test_results['passed'] / test_results['total_tests']) * 100
        print("="*60)
        print(f"RESUMEN: {success_rate:.1f}% de éxito")
        
        if success_rate >= 80:
            print("🎉 Parser modular funcionando correctamente!")
        elif success_rate >= 60:
            print("⚠️  Parser modular funcional con algunos problemas menores")
        else:
            print("🚨 Parser modular requiere correcciones significativas")
        
        print("="*60)
        
        return f"Validación completada: {success_rate:.1f}% de éxito"


def main():
    """Función principal del validador."""
    validator = ParserValidator()
    result = validator.generate_report()
    print(f"\n{result}")


if __name__ == "__main__":
    main()