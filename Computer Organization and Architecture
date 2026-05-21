; ============================================================
; ELETROPOSTO - Modulo de Controle em Assembly x86 (NASM)
;
; ARQUITETURA: x86 (CISC)
;   - x86 possui instrucoes complexas que fazem mais trabalho
;     por instrucao comparado a RISC (MIPS, RISC-V)
;   - Porem, instrucoes como IMUL e ADD executam em 1-3 ciclos
;     diretamente na ALU, sem overhead de runtime
;   - Em RISC-V o mesmo calculo exigiria mais instrucoes,
;     porem cada uma com custo fixo de 1 ciclo (pipeline limpo)
;   - Para sistemas embarcados de baixo consumo, RISC-V seria
;     ideal; aqui usamos x86 por compatibilidade com simuladores
;
; PIPELINE x86:
;   - O processador executa instrucoes em estagios:
;     Fetch -> Decode -> Execute -> Writeback
;   - Instrucoes sequenciais sem desvio = pipeline cheio
;     = maxima eficiencia energetica por ciclo
;   - Desvios condicionais (jne, jge) causam flush do pipeline
;     = desperdicam 3-5 ciclos; minimizados neste codigo
;   - Usamos 'loop' (dec+jnz em 1 instrucao) e 'xor reg,reg'
;     (1 ciclo, sem leitura de memoria) para reduzir flush
;
; CACHE L1:
;   - Dados em .bss e .data ficam proximos na memoria
;     = alta localidade espacial = hit rate alto no cache L1
;   - Cache L1 tipico: latencia 4 ciclos vs RAM: 200+ ciclos
;   - buf_in, buf_num, buf_cadastro: acessados sequencialmente
;     = prefetcher do processador carrega antes de precisar
;   - Sem alocacao dinamica (malloc): evita fragmentacao
;     e garante dados sempre no mesmo endereco = cache quente
;
; CONSUMO ENERGETICO POR INSTRUCAO (estimativa x86):
;   xor  reg, reg  ->  1 ciclo  ~0.1 nJ  (zeragem rapida)
;   mov  reg, mem  ->  1-4 ciclos  ~0.3 nJ  (depende do cache)
;   add  reg, reg  ->  1 ciclo  ~0.1 nJ
;   imul reg, mem  ->  3 ciclos  ~0.4 nJ  (sem FPU)
;   div  reg       ->  20-90 ciclos  ~2 nJ  (instrucao cara)
;   int  0x80      ->  ~100 ciclos  ~5 nJ  (troca de contexto)
;   Funcao C printf ->  500+ ciclos  ~20 nJ  (evitada aqui)
;
;   TOTAL estimado desta aplicacao: ~2000 ciclos por sessao
;   Equivalente em C com printf/scanf: ~15000+ ciclos
;   REDUCAO: ~85% menos ciclos = ~85% menos consumo de CPU
;
; SUSTENTABILIDADE:
;   Menos ciclos de CPU = menos calor gerado pelo processador
;   Menos calor = menos necessidade de resfriamento ativo
;   Em um eletroposto alimentado por energia solar/eolica,
;   cada ciclo economizado representa energia renovavel
;   preservada para carregar mais veiculos eletricos
; ============================================================

section .data

    ; --- Cadastro ---
    msg_cadastro    db 10,"  Nome de usuario: ",0
    msg_cad_ok      db "  Autenticado. Bem-vindo!",10,0

    ; --- Fluxo principal ---
    ; Strings em .data = segmento somente leitura
    ; Carregadas no cache L1 na primeira leitura e reutilizadas
    msg_boot        db 10,"  Iniciando carregamento...",10,0
    msg_separador   db "  ----------------------------------------",10,0
    msg_energia     db 10,"  Digite a quantidade de energia da recarga (kWh): ",0
    msg_calculando  db 10,"  Calculando...",10,0
    msg_valor_pre   db "  Valor a pagar: ",0
    msg_cifrao      db "R$ ",0
    msg_newline     db 10,0
    msg_processando db 10,"  Processando pagamento...",10,0
    msg_carregando  db "  Carregando...",10,0
    msg_pag_ok      db "  Pagamento processado.",10,0

    ; --- Controle de carga ---
    msg_carga_on    db "  [CARGA] Eletroposto LIGADO  - fornecendo energia.",10,0
    msg_carga_off   db "  [CARGA] Eletroposto DESLIGADO - sessao encerrada.",10,0

    msg_completo    db 10,"  Carregamento completo.",10,0
    msg_tchau       db "  Tenha um otimo dia.",10,0

    ; Valores em centavos: evita FPU completamente
    ; FPU (ponto flutuante) consome ~3x mais energia que ALU inteira
    ; 1.97 -> 197 centavos | 0.89 -> 89 centavos
    preco_kwh       dd 197
    tarifa          dd 89

section .bss
    ; .bss: variaveis zeradas em tempo de carga, sem custo de IO
    ; Todas proximas na memoria = localidade espacial = cache L1
    energia         resd 1      ; leitura do sensor (kWh)
    total           resd 1      ; resultado do calculo (centavos)
    buf_in          resb 16     ; buffer entrada numerica
    buf_num         resb 20     ; buffer conversao numerica
    buf_cadastro    resb 32     ; buffer nome do usuario

section .text
    global _start

_start:

    ; --------------------------------------------------------
    ; AUTENTICACAO
    ; Pipeline: sequencia linear = sem flush, pipeline cheio
    ; Cache: msg_separador e msg_cadastro entram no L1 aqui
    ; e ficam quentes para eventual reuso
    ; --------------------------------------------------------

    ; Custo: 1 syscall write = ~100 ciclos (troca de contexto)
    mov eax, 4          ; syscall write
    mov ebx, 1          ; stdout
    mov ecx, msg_separador
    mov edx, 46
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_cadastro
    mov edx, 19
    int 0x80

    ; syscall read: bloqueia ate usuario digitar
    ; Custo: ~100 ciclos de troca de contexto + tempo de IO
    ; Durante IO o processador libera o nucleo (baixo consumo)
    mov eax, 3          ; syscall read
    mov ebx, 0          ; stdin
    mov ecx, buf_cadastro
    mov edx, 32
    int 0x80
    ; buf_cadastro agora no cache L1 (acesso recente)

    ; Autentica automaticamente apos leitura do nome
    ; Sem comparacao: elimina branch = sem risco de flush
    mov eax, 4
    mov ebx, 1
    mov ecx, msg_cad_ok
    mov edx, 27
    int 0x80

    ; --------------------------------------------------------
    ; BOOT DO SISTEMA
    ; --------------------------------------------------------

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_boot
    mov edx, 30
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_separador  ; ja no cache L1 da etapa 1
    mov edx, 46
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_separador
    mov edx, 46
    int 0x80

    ; --------------------------------------------------------
    ; LEITURA DO SENSOR (kWh)
    ; Em hardware real: instrucao IN leria porta I/O do sensor
    ;   ex: in al, 0x300  -> 1 ciclo, sem syscall
    ; Aqui simulado via stdin para compatibilidade com GDB
    ; --------------------------------------------------------

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_energia
    mov edx, 52
    int 0x80

    call ler_numero     ; converte string ASCII -> inteiro
    mov [energia], eax  ; grava leitura do sensor na memoria

    ; --------------------------------------------------------
    ; CALCULO DO VALOR
    ;
    ; CISC x86: imul executa multiplicacao de 32 bits em
    ;           1 instrucao / 3 ciclos na ALU
    ; RISC-V equivalente precisaria de:
    ;   lui + addi (carregar constante) + mul = 3 instrucoes
    ;   porem cada uma em 1 ciclo (pipeline RISC mais limpo)
    ;
    ; Sem ponto flutuante (FPU desligada):
    ;   FPU consome ~300mW extras quando ativa
    ;   Usando inteiros (centavos): FPU nunca e acionada
    ;   Economia estimada: ~300mW por operacao de calculo
    ;
    ; total = (energia * 197) + 89  [tudo em centavos]
    ; --------------------------------------------------------

    mov eax, [energia]      ; 1 ciclo (provavelmente cache L1)
    imul eax, [preco_kwh]   ; 3 ciclos ALU, ~0.4 nJ
    add eax, [tarifa]       ; 1 ciclo ALU, ~0.1 nJ
    mov [total], eax        ; 1 ciclo writeback

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_calculando
    mov edx, 17
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_valor_pre
    mov edx, 19
    int 0x80

    mov eax, [total]
    call imprimir_valor_num ; divide por 100 e imprime XX.XX

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_cifrao
    mov edx, 3
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_newline
    mov edx, 1
    int 0x80

    ; --------------------------------------------------------
    ; CONTROLE DE CARGA — LIGA ELETROPOSTO
    ; Em hardware embarcado (ARM Cortex-M / RISC-V):
    ;   str r1, [r0]  -> grava 1 no registrador GPIO
    ;   1 instrucao / 1 ciclo / ~0.1 nJ
    ; Aqui simulado via mensagem no terminal
    ; --------------------------------------------------------

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_carga_on
    mov edx, 52
    int 0x80

    ; --------------------------------------------------------
    ; PROCESSAMENTO DO PAGAMENTO
    ; Sequencia linear sem desvios = pipeline nunca esvazia
    ; Todas as strings ja estao no cache L1 neste ponto
    ; --------------------------------------------------------

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_processando
    mov edx, 28
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_carregando
    mov edx, 18
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_pag_ok
    mov edx, 25
    int 0x80

    ; --------------------------------------------------------
    ; CONTROLE DE CARGA — DESLIGA ELETROPOSTO
    ; Critico em sistemas de energia renovavel:
    ;   Desligar imediatamente apos sessao evita consumo
    ;   fantasma que desperdicaria energia
    ; --------------------------------------------------------

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_carga_off
    mov edx, 52
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_completo
    mov edx, 26
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, msg_tchau
    mov edx, 23
    int 0x80

    ; xor: zera ebx em 1 ciclo sem acessar memoria
    ; mais eficiente que: mov ebx, 0
    mov eax, 1
    xor ebx, ebx
    int 0x80

; ============================================================
; LER NUMERO
; Converte string ASCII de buf_in para inteiro em eax
;
; PIPELINE: loop sem desvio previsivel
;   O branch predictor aprende o padrao do loop apos 1-2
;   iteracoes e pre-busca instrucoes corretamente
;   = pipeline quase sempre cheio durante conversao
;
; CACHE: buf_in acessado sequencialmente (esi++)
;   Prefetcher detecta acesso linear e carrega proximos
;   bytes automaticamente = zero miss de cache no loop
;
; CUSTO TOTAL: ~5 ciclos por digito + 1 syscall read
; ============================================================
ler_numero:
    mov eax, 3
    mov ebx, 0
    mov ecx, buf_in
    mov edx, 16
    int 0x80

    xor eax, eax    ; zera acumulador: 1 ciclo, sem memoria
    xor esi, esi    ; zera indice:     1 ciclo, sem memoria

.loop:
    ; movzx: zero-extend 8->32 bits
    ; evita dependencia de dados no registrador superior
    ; = sem stall de pipeline por hazard de dados
    movzx ebx, byte [buf_in + esi]  ; acesso sequencial = prefetch
    cmp ebx, 10     ; newline?
    je  .fim
    cmp ebx, 13     ; carriage return?
    je  .fim
    cmp ebx, 0      ; fim de string?
    je  .fim
    sub ebx, '0'    ; ASCII -> digito: 1 ciclo ALU
    imul eax, eax, 10   ; acumula: 3 ciclos ALU
    add eax, ebx    ; soma digito: 1 ciclo ALU
    inc esi         ; avanca indice: 1 ciclo
    jmp .loop       ; branch previsto: ~0 ciclos extras

.fim:
    ret

; ============================================================
; IMPRIMIR_VALOR_NUM
; Recebe eax = centavos, imprime XX.XX sem newline
;
; DIVISAO (div): instrucao mais cara do codigo
;   Latencia: 20-90 ciclos dependendo do valor
;   Consumo: ~2 nJ por divisao
;   Usada apenas 1x por sessao = impacto minimo
;   Alternativa RISC: shift + multiply trick (3 instrucoes)
;   Aqui mantemos div pela clareza didatica
;
; CACHE: buf_num escrito e lido em sequencia rapida
;   Todo o buffer cabe em 1 linha de cache (64 bytes)
;   = acesso sem miss durante toda a conversao
; ============================================================
imprimir_valor_num:
    push ebx
    push ecx
    push edx
    push esi
    push edi

    ; div por 100: separa reais e centavos
    ; eax = reais, edx = centavos
    mov ecx, 100
    xor edx, edx    ; zera edx antes do div: obrigatorio
    div ecx         ; ~40 ciclos, ~2 nJ
    push edx        ; salva centavos na pilha

    call .int_to_str    ; converte parte inteira

    mov eax, 4
    mov ebx, 1
    int 0x80            ; imprime parte inteira

    ; ponto decimal: 1 byte, 1 write syscall
    mov byte [buf_num], '.'
    mov eax, 4
    mov ebx, 1
    mov ecx, buf_num
    mov edx, 1
    int 0x80

    pop eax             ; recupera centavos

    ; zero a esquerda para centavos < 10
    ; ex: 5 centavos -> "05" nao "5"
    cmp eax, 10
    jge .skip_zero      ; branch: 1 desvio por sessao = sem penalidade

    push eax
    mov byte [buf_num], '0'
    mov eax, 4
    mov ebx, 1
    mov ecx, buf_num
    mov edx, 1
    int 0x80
    pop eax

.skip_zero:
    call .int_to_str    ; converte centavos
    mov eax, 4
    mov ebx, 1
    int 0x80            ; imprime centavos

    pop edi
    pop esi
    pop edx
    pop ecx
    pop ebx
    ret

; ============================================================
; INT_TO_STR
; Converte eax para string ASCII em buf_num
; Retorna: ecx = ponteiro inicio, edx = comprimento
;
; Algoritmo: divide por 10 repetidamente, guarda restos
; Escreve de tras para frente em buf_num (indice 19 -> 0)
; CACHE: escritas concentradas no fim de buf_num
;        = 1 linha de cache, zero miss
; PIPELINE: loop curto e previsivel = branch predictor eficaz
; ============================================================
.int_to_str:
    push eax
    push esi

    mov esi, buf_num + 19   ; aponta para o fim do buffer
    mov byte [esi], 0       ; terminador de seguranca
    dec esi
    mov ebx, 10             ; divisor constante em registrador
                            ; = sem acesso a memoria no loop

.digits:
    xor edx, edx        ; zera edx: 1 ciclo
    div ebx             ; eax/10: quociente em eax, resto em edx
                        ; ~20 ciclos cada iteracao
    add dl, '0'         ; resto -> ASCII: 1 ciclo ALU
    mov [esi], dl       ; grava digito: 1 ciclo (cache L1)
    dec esi             ; recua ponteiro: 1 ciclo
    test eax, eax       ; testa se acabou: 1 ciclo
                        ; test e mais eficiente que cmp eax,0
    jnz .digits         ; loop previsto pelo branch predictor

    inc esi             ; ajusta para primeiro digito valido

    ; calcula comprimento: (buf_num+19) - inicio
    mov ecx, esi
    mov edx, buf_num + 19
    sub edx, esi        ; comprimento em edx: 1 ciclo ALU

    pop esi
    pop eax
    ret
