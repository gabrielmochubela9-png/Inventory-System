var T;
function render(i){var m=$('#main');[dash,stock,move,hist][i](m)}
T=tabs(['Dashboard','Stock','Receive and issue','History'],render);
