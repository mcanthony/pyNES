# -*- coding: utf-8 -*-

import unittest
import ast

from pynes.asm import *
from pynes.block import AsmBlock


class AsmBlockOperationTest(unittest.TestCase):


    def assert_expr(self, expr, code):
        self.assertEquals(str(expr), code)

    def assert_type(self, obj, type_name, instruction_name=None, address_mode=None):
        self.assertEquals(type(obj).__name__, type_name)
        if (instruction_name):
            self.assertEquals(obj.name, instruction_name)
        if (address_mode):
            self.assertEquals(obj.address_mode, address_mode)

    def test_lda_plus_one_returns_immediate_instruction(self):
        result = LDA + 1
        self.assert_type(result, 'Instruction')
        self.assertEquals(result.address_mode, 'imm')

    def test_lda_plus_one_returns_immediate_instruction(self):
        result = LDA + 1 + CLC
        self.assert_type(result, 'AsmBlock')
        self.assert_type(result.get(0), 'Instruction', 'LDA')
        self.assert_type(result.get(1), 'Instruction', 'CLC')

    def test_lda_plus_one_returns_asmblock(self):
        result = LDA + 1 + CLC + ADC
        self.assert_type(result, 'AsmBlock')
        self.assertEquals(len(result), 3)
        self.assert_type(result.get(0), 'Instruction', 'LDA')
        self.assert_type(result.get(1), 'Instruction', 'CLC')
        self.assert_type(result.get(2), 'InstructionProxy', 'ADC')


    def test_complete_sum(self):
        result = LDA + 1 + CLC + ADC + 1
        self.assert_type(result, 'AsmBlock')
        self.assertEquals(len(result), 3)
        self.assert_type(result.get(0), 'Instruction', 'LDA', 'imm')
        self.assert_type(result.get(1), 'Instruction', 'CLC', 'sngl')
        self.assert_type(result.get(2), 'Instruction', 'ADC', 'imm')
        actual = str(result)
        expected = '\n'.join([
                'LDA #1',
                'CLC',
                'ADC #1'
            ]) + '\n'
        self.assertEquals(actual, expected)


    def test_adc_plus_one_returns_immediate_instruction(self):
        result = ADC + 1
        self.assert_type(result, 'Instruction')
        self.assertEquals(result.address_mode, 'imm')

    def test_cpm_plus_zp_string_returns_zeropage_instruction(self):
        result = CMP + '$44'
        self.assert_type(result, 'Instruction')
        self.assertEquals(result.address_mode, 'zp')

    def test_cpm_plus_absolute_addr_returns_zeropage_instruction(self):
        result = CMP + '$4400'
        self.assert_type(result, 'Instruction')
        self.assertEquals(result.address_mode, 'abs')

    def test_call_a_sngl_proxy_returns_a_instruction(self):
        result = CLC()
        self.assert_type(result, 'Instruction')
        self.assertEquals(result.address_mode, 'sngl')

    def test_call_immediate_proxy_with_int_returns_instruction(self):
        result = ADC(1)
        self.assert_type(result, 'Instruction')
        self.assertEquals(result.address_mode, 'imm')        

    def test_adc_plus_two_returns_immediate_instruction_2(self):
        result = ADC + 2
        self.assert_type(result, 'Instruction')
        self.assertEquals(result.address_mode, 'imm')

    def test_instruction_plus_instruction_returns_asmblock(self):
        instruction_1 = ADC + 1
        instruction_2 = ADC + 2
        result = instruction_1 + instruction_2
        self.assert_type(result, 'AsmBlock')
        self.assert_type(result.get(0), 'Instruction')
        self.assert_type(result.get(1), 'Instruction')

    def test_clc_plus_adc_returns_asmblock_with_instruction_and_instruction_proxy(self):
        result = CLC + ADC
        self.assert_type(result, 'AsmBlock')
        self.assertEquals(len(result), 2)
        self.assert_type(result.get(0), 'Instruction')
        self.assert_type(result.get(1), 'InstructionProxy')

    def test_clc_adc_one_returns_asmblock_with_two_instructions(self):
        result = CLC + ADC + 1
        self.assert_type(result, 'AsmBlock')
        self.assertEquals(len(result), 2)
        self.assert_type(result.get(0), 'Instruction')
        self.assert_type(result.get(1), 'Instruction')
        actual = str(result)
        expected = '\n'.join([
                'CLC',
                'ADC #1'
            ]) + '\n'
        self.assertEquals(actual, expected)

    def test_asmblock_with_instruction_and_instruction_proxy_plus_one_returns_asmblock_with_two_instructions(self):
        return
        result = AsmBlock(CLC, ADC) + 1;
        self.assert_type(result, 'AsmBlock')
        self.assertEquals(len(result), 2)
        self.assert_type(result.get(0), 'Instruction')
        # self.assert_type(result.get(1), 'Instruction')
        # actual = str(result)
        # expected = '\n'.join([
        #         'CLC',
        #         'ADC #1'
        #     ]) + '\n'
        # self.assertEquals(actual, expected)


    def test_expression_asl_plus_a(self):
        self.assert_expr(ASL + A, 'ASL A')
        # self.assert_expr(ASL(A), 'ASL A')

    def test_eee(self):
        self.assert_expr(ADC + 0x0a, 'ADC #10')

    def test_ee1(self):
        return
        result = ADC + '$10'
        actual = str(result)
        expected = 'ADC $10'
        self.assertEquals(actual, expected)

    def test_fff(self):
        return
        result = ADC + ['$10', X]
        actual = str(result)
        expected = 'ADC $10, X'
        self.assertEquals(actual, expected)
