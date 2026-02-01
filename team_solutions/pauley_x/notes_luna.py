def get_syndrome(measurements):
            syndrome:int = 0
            for stab in range(3):
                eigval = 1
                for idx in stabilizers[stab]:
                    if measurements[idx]:
                        eigval = eigval*-1
                        if eigval == -1:
                            squin.x[0]
                if eigval == 1:
                    syndrome += (2**stab)
            return syndrome
        
        # def get_syndromes(eigenvalues, stabilizers):
        #     syndrome = []
        #     for stab in stabilizers:
        #         eigval = 1
        #         for idx in stab:
        #             eigval *= eigenvalues[idx]
        #         syndrome.append(eigval)
        #         syndrome = tuple(syndrome)
        #         syndrome = get_int(syndrome)
        #     return syndrome
        
        # def update_pauli_corrections_from_syndrome(current_pauli_list, syndrome, syndrome_table):
        #     if syndrome!=7:
        #         index = syndrome_table[syndrome]
        #         if current_pauli_list[index] == 0:
        #             current_pauli_list[index] = 1
        #         else:
        #             current_pauli_list[index] = 0

        syndrome = get_syndrome(z_measurement)
        if syndrome != 7:
            index = syndrome_table[syndrome]
            squin.x[index]
