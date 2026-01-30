// tt_um_ay5876_d_flip_flop.v
// TinyTapeout user module: D Flip-Flop (posedge clk, async active-low reset)

module tt_um_ay5876_d_flip_flop (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: input path
    output wire [7:0] uio_out,  // IOs: output path
    output wire [7:0] uio_oe,   // IOs: enable (1=drive)
    input  wire       ena,      // Always 1 when active (can ignore safely)
    input  wire       clk,      // Clock
    input  wire       rst_n      // Async reset (active low)
);

    // Use ui_in[0] as D input
    wire din = ui_in[0];

    // Flip-flop state
    reg q;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 1'b0;
        else
            q <= din;
    end

    // Output mapping:
    // uo_out[0] = Q
    // uo_out[1] = ~Q
    assign uo_out[0] = q;
    assign uo_out[1] = ~q;

    // All other outputs must be driven (avoid warnings)
    assign uo_out[7:2] = 6'b0;

    // Disable bidirectional IO driving
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Mark unused inputs so lint/synth don't complain
    wire _unused = |uio_in | ena | ui_in[7:1];

endmodule
