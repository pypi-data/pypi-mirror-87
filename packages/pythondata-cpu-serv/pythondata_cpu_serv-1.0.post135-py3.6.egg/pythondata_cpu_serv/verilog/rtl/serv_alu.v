`default_nettype none
module serv_alu
  (
   input wire 	    clk,
   input wire 	    i_en,
   input wire 	    i_shift_op,
   input wire 	    i_cnt0,
   input wire 	    i_rs1,
   input wire 	    i_rs2,
   input wire 	    i_imm,
   input wire 	    i_op_b_rs2,
   input wire 	    i_buf,
   input wire 	    i_init,
   input wire 	    i_cnt_done,
   input wire 	    i_sub,
   input wire [1:0] i_bool_op,
   input wire 	    i_cmp_eq,
   input wire 	    i_cmp_sig,
   output wire 	    o_cmp,
   input wire 	    i_shamt_en,
   input wire 	    i_sh_right,
   input wire 	    i_sh_signed,
   output wire 	    o_sh_done,
   input wire [3:0] i_rd_sel,
   output wire 	    o_rd);

   wire        result_add;
   wire        result_eq;
   wire        result_sh;

   reg 	       result_lt_r;

   reg [4:0]   shamt;
   reg 	       shamt_msb;

   wire        add_cy;
   reg 	       add_cy_r;

   wire op_b = i_op_b_rs2 ? i_rs2 : i_imm;

   serv_shift shift
     (
      .i_clk (clk),
      .i_load (i_init),
      .i_shamt (shamt),
      .i_shamt_msb (shamt_msb),
      .i_signbit (i_sh_signed & i_rs1),
      .i_right  (i_sh_right),
      .o_done   (o_sh_done),
      .i_d (i_buf),
      .o_q (result_sh));

   //Sign-extended operands
   wire rs1_sx  = i_rs1 & i_cmp_sig;
   wire op_b_sx = op_b  & i_cmp_sig;

   wire result_lt = rs1_sx + ~op_b_sx + add_cy;

   wire add_a = i_rs1 & ~i_shift_op;
   wire add_b = op_b^i_sub;

   assign {add_cy,result_add}   = add_a+add_b+add_cy_r;

   reg        eq_r;

   assign result_eq = !result_add & eq_r;

   assign o_cmp = i_cmp_eq ? result_eq : result_lt;

   localparam [15:0] BOOL_LUT = 16'h8E96;//And, Or, =, xor
   wire result_bool = BOOL_LUT[{i_bool_op, i_rs1, op_b}];

   assign o_rd = (i_rd_sel[0] & result_add) |
                 (i_rd_sel[1] & result_sh) |
                 (i_rd_sel[2] & result_lt_r & i_cnt0) |
                 (i_rd_sel[3] & result_bool);


   always @(posedge clk) begin
      add_cy_r <= i_en ? add_cy : i_sub;

      if (i_en) begin
	 result_lt_r <= result_lt;
      end
      eq_r <= result_eq | ~i_en;

      if (i_shamt_en) begin
	 shamt_msb <= add_cy;
	 shamt <= {result_add,shamt[4:1]};
      end
   end

endmodule
