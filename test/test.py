import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def set_d(dut, d_bit):
    # ui_in is 8-bit bus. Put D on bit0, keep others 0.
    dut.ui_in.value = (1 if d_bit else 0)

def get_q(dut):
    # uo_out is 8-bit bus. Q is bit0.
    return int(dut.uo_out.value) & 1

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Manual-style clock
    clock = Clock(dut.clk, 10, units="us")
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

    dut._log.info("Test project behavior")

    # Manual-style stimulus sequence (but no [0] indexing)
    set_d(dut, 0)
    await ClockCycles(dut.clk, 20)
    assert get_q(dut) == 0

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)

    dut.rst_n.value = 1
    set_d(dut, 1)
    await ClockCycles(dut.clk, 20)
    assert get_q(dut) == 1

    set_d(dut, 0)
    await ClockCycles(dut.clk, 1)
    assert get_q(dut) == 0

    set_d(dut, 1)
    await ClockCycles(dut.clk, 20)
    assert get_q(dut) == 1

    set_d(dut, 0)
    await ClockCycles(dut.clk, 10)
    assert get_q(dut) == 0
