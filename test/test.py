# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period (unit doesn't matter; keep it consistent)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("Test DFF behavior")

    # After reset, Q should be 0
    assert int(dut.uo_out[0].value) == 0

    # D=0 -> Q stays 0 on next clock
    dut.ui_in[0].value = 0
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out[0].value) == 0

    # D=1 -> Q becomes 1 on next clock
    dut.ui_in[0].value = 1
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out[0].value) == 1

    # D=0 -> Q becomes 0 on next clock
    dut.ui_in[0].value = 0
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out[0].value) == 0

