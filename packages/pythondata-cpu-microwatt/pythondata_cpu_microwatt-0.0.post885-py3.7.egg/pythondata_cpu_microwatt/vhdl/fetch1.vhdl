library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.common.all;

entity fetch1 is
    generic(
	RESET_ADDRESS     : std_logic_vector(63 downto 0) := (others => '0');
	ALT_RESET_ADDRESS : std_logic_vector(63 downto 0) := (others => '0')
	);
    port(
	clk           : in std_ulogic;
	rst           : in std_ulogic;

	-- Control inputs:
	stall_in      : in std_ulogic;
	flush_in      : in std_ulogic;
	stop_in       : in std_ulogic;
	alt_reset_in  : in std_ulogic;

	-- redirect from execution unit
	e_in          : in Execute1ToFetch1Type;

        -- redirect from decode1
        d_in          : in Decode1ToFetch1Type;

	-- Request to icache
	i_out         : out Fetch1ToIcacheType;

        -- outputs to logger
        log_out       : out std_ulogic_vector(42 downto 0)
	);
end entity fetch1;

architecture behaviour of fetch1 is
    type stop_state_t is (RUNNING, STOPPED, RESTARTING);
    type reg_internal_t is record
	stop_state: stop_state_t;
        mode_32bit: std_ulogic;
    end record;
    signal r, r_next : Fetch1ToIcacheType;
    signal r_int, r_next_int : reg_internal_t;
    signal log_nia : std_ulogic_vector(42 downto 0);
begin

    regs : process(clk)
    begin
	if rising_edge(clk) then
            log_nia <= r.nia(63) & r.nia(43 downto 2);
	    if r /= r_next then
		report "fetch1 rst:" & std_ulogic'image(rst) &
                    " IR:" & std_ulogic'image(r_next.virt_mode) &
                    " P:" & std_ulogic'image(r_next.priv_mode) &
                    " E:" & std_ulogic'image(r_next.big_endian) &
                    " 32:" & std_ulogic'image(r_next_int.mode_32bit) &
		    " R:" & std_ulogic'image(e_in.redirect) & std_ulogic'image(d_in.redirect) &
		    " S:" & std_ulogic'image(stall_in) &
		    " T:" & std_ulogic'image(stop_in) &
		    " nia:" & to_hstring(r_next.nia) &
		    " SM:" & std_ulogic'image(r_next.stop_mark);
	    end if;
	    r <= r_next;
	    r_int <= r_next_int;
	end if;
    end process;
    log_out <= log_nia;

    comb : process(all)
	variable v : Fetch1ToIcacheType;
	variable v_int : reg_internal_t;
	variable increment : boolean;
    begin
	v := r;
	v_int := r_int;
        v.sequential := '0';

	if rst = '1' then
	    if alt_reset_in = '1' then
		v.nia :=  ALT_RESET_ADDRESS;
	    else
		v.nia :=  RESET_ADDRESS;
	    end if;
            v.virt_mode := '0';
            v.priv_mode := '1';
            v.big_endian := '0';
	    v_int.stop_state := RUNNING;
            v_int.mode_32bit := '0';
	elsif e_in.redirect = '1' then
	    v.nia := e_in.redirect_nia(63 downto 2) & "00";
            if e_in.mode_32bit = '1' then
                v.nia(63 downto 32) := (others => '0');
            end if;
            v.virt_mode := e_in.virt_mode;
            v.priv_mode := e_in.priv_mode;
            v.big_endian := e_in.big_endian;
            v_int.mode_32bit := e_in.mode_32bit;
        elsif d_in.redirect = '1' then
            v.nia := d_in.redirect_nia(63 downto 2) & "00";
            if r_int.mode_32bit = '1' then
                v.nia(63 downto 32) := (others => '0');
            end if;
	elsif stall_in = '0' then

	    -- For debug stop/step to work properly we need a little bit of
	    -- trickery here. If we just stop incrementing and send stop marks
	    -- when stop_in is set, then we'll increment on the cycle it clears
	    -- and end up never executing the instruction we were stopped on.
	    --
	    -- Avoid this along with the opposite issue when stepping (stop is
	    -- cleared for only one cycle) is handled by the state machine below
	    --
	    -- By default, increment addresses
	    increment := true;
	    case v_int.stop_state is
	    when RUNNING =>
		-- If we are running and stop_in is set, then stop incrementing,
		-- we are now stopped.
		if stop_in = '1' then
		    increment := false;
		    v_int.stop_state := STOPPED;
		end if;
	    when STOPPED =>
		-- When stopped, never increment. If stop is cleared, go to state
		-- "restarting" but still don't increment that cycle. stop_in is
		-- now 0 so we'll send the NIA down without a stop mark.
		increment := false;
		if stop_in = '0' then
		    v_int.stop_state := RESTARTING;
		end if;
	    when RESTARTING =>
		-- We have just sent the NIA down, we can start incrementing again.
		-- If stop_in is still not set, go back to running normally.
		-- If stop_in is set again (that was a one-cycle "step"), go
		-- back to "stopped" state which means we'll stop incrementing
		-- on the next cycle. This ensures we increment the PC once after
		-- sending one instruction without a stop mark. Since stop_in is
		-- now set, the new PC will be sent with a stop mark and thus not
		-- executed.
		if stop_in = '0' then
		    v_int.stop_state := RUNNING;
		else
		    v_int.stop_state := STOPPED;
		end if;
	    end case;

	    if increment then
                if r_int.mode_32bit = '0' then
                    v.nia := std_ulogic_vector(unsigned(r.nia) + 4);
                else
                    v.nia := x"00000000" & std_ulogic_vector(unsigned(r.nia(31 downto 0)) + 4);
                end if;
                v.sequential := '1';
	    end if;
	end if;

	v.req := not rst;
	v.stop_mark := stop_in;

	r_next <= v;
	r_next_int <= v_int;

	-- Update outputs to the icache
	i_out <= r;

    end process;

end architecture behaviour;
