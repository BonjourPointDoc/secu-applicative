// client_tls.c
#include <netinet/in.h>
#include <openssl/bio.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/rsa.h>
#include <netdb.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include <sys/random.h>

// Compile :
// gcc client_tls.c -o client_tls -lssl -lcrypto

/**
 * @brief Checks the arguments provided to CLI
 * 
 * @param argc 
 * @param argv 
 * @param loop_counter 
 * @return int 
 */
int check_arguments(int argc, char **argv, long *loop_counter)
{
    // Check parameters
    if(argc != 2)
    {
        fprintf(stderr, "Argument missing.\nUsage : test_tls [arg]\n[arg] : Integer used to count the cypher/decypher loop.\n");
        exit(EXIT_FAILURE);
    }

    char *endptr = NULL;
    errno = 0;  // Reinit errno
    *loop_counter = strtol(argv[1], &endptr, 10);

    if(errno == ERANGE)
    {
        fprintf(stderr, "Bad argument provided: %s, OVERFLOW/UNDERFLOW detected\nUsage : test_tls [arg]\n[arg] : Integer used to count the cypher/decypher loop.\n", argv[1]);
        exit(EXIT_FAILURE);
    }
    else if(*endptr != '\0')
    {
        fprintf(stderr, "Bad argument provided: %s, usage of bad characters detected ('%s')\nUsage : test_tls [arg]\n[arg] : Integer used to count the cypher/decypher loop.\n", argv[1], endptr);
        exit(EXIT_FAILURE);
    }

    if(*loop_counter <= 0)
    {
        fprintf(stderr, "Bad argument provided: %s, use a non-zero, positive value\nUsage : test_tls [arg]\n[arg] : Integer used to count the cypher/decypher loop.\n", argv[1]);
        exit(EXIT_FAILURE);
    }
    return 0;
}

/**
 * @brief Send until full alea send to server
 * 
 * @param ssl 
 * @param data 
 * @param len 
 * @return int 
 */
int send_full_data(SSL *ssl, const unsigned char *data, size_t len)
{
    size_t total_sent = 0;
    while(total_sent < len)
    {
        int n = SSL_write(ssl, data + total_sent, len - total_sent);
        if(n <= 0)
        {
            int ssl_error = SSL_get_error(ssl, n);
            fprintf(stderr, "Erreur SSL_write: %d\n", ssl_error);
            return -1;
        }
        total_sent += n;
    }
    return 0;
}

/**
 * @brief Read from ssl until full data acquired
 * 
 * @param ssl 
 * @param data 
 * @param len 
 * @return int 
 */
int recv_full_data(SSL *ssl, unsigned char *data, size_t len)
{
    size_t total_received = 0;
    while(total_received < len)
    {
        int n = SSL_read(ssl, data + total_received, len - total_received);
        if(n <= 0)
        {
            int ssl_error = SSL_get_error(ssl, n);
            if(ssl_error == SSL_ERROR_ZERO_RETURN)
            {
                fprintf(stderr, "Connexion closed by server\n");
            }
            else
            {
                fprintf(stderr, "Erreur SSL_read: %d\n", ssl_error);
            }
            return -1;
        }
        total_received += n;
    }
    return 0;
}


/**
 * @brief Just used for some debugging, shows a part of the returned signed alea value
 * 
 * @param data 
 * @param len 
 * @param label 
 */
void print_hex(const unsigned char *data, size_t len, const char *label)
{
    printf("%s: ", label);
    for(size_t i = 0; i < len && i < 16; i++)
    {
        printf("%02x ", data[i]);
    }
    if(len > 16) printf("... (total: %zu bytes)", len);
    printf("\n");
}




// ------------------------------------------------------------------------------

int main(int argc, char **argv) 
{
    long loop_counter;
    // Check arguments provided
    if(check_arguments(argc, argv, &loop_counter))
    {
        exit(EXIT_FAILURE);
    }

    // Init SSL
    SSL_library_init();
    SSL_load_error_strings();
    const SSL_METHOD *method = TLS_client_method();
    SSL_CTX *ctx = SSL_CTX_new(method);
    EVP_PKEY *pkey = NULL;

    if (!ctx) {
        ERR_print_errors_fp(stderr);
        return 1;
    }

    // Socket creation
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if(sock < 0)
    {
        perror("Erreur création socket");
        return 1;
    }

    struct hostent *host = gethostbyname("127.0.0.1");
    if(!host)
    {
        fprintf(stderr, "Erreur résolution hostname\n");
        return 1;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8443);
    addr.sin_addr = *((struct in_addr*) host->h_addr);
    memset(&(addr.sin_zero), 0, 8);

    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) != 0) {
        perror("Erreur de connexion");
        return 1;
    }

    // Create SSL session and links it to opened socket
    SSL *ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sock);

    // Handshake
    if (SSL_connect(ssl) != 1)
    {
        fprintf(stderr, "Erreur handshake SSL\n");
        ERR_print_errors_fp(stderr);
        return 1;
    }

    printf("SSL Connexion OK\n");

    // Get public key from server
    char buf[4096] = {0};
    int total_read = 0;
    
    // Get public key
    while(total_read < sizeof(buf) - 1)
    {
        int len = SSL_read(ssl, buf + total_read, sizeof(buf) - total_read - 1);
        if(len <= 0)
        {
            if(total_read > 0) break;
            fprintf(stderr, "Erreur lecture clé publique\n");
            return 1;
        }
        total_read += len;
        
        // Check the end of the pub key
        if(strstr(buf, "-----END PUBLIC KEY-----"))
        {
            break;
        }
    }
    
    buf[total_read] = '\0';
    printf("Pub key received reçue (%d bytes):\n%s\n", total_read, buf);

    // Create BIO to read public key from string
    BIO *bio = BIO_new_mem_buf(buf, -1);
    if (!bio) {
        fprintf(stderr, "BIO creation error\n");
        return 1;
    }

    // Extract key from BIO
    pkey = PEM_read_bio_PUBKEY(bio, NULL, NULL, NULL);
    BIO_free(bio);
    if(!pkey)
    {
        fprintf(stderr, "Public key extraction error\n");
        ERR_print_errors_fp(stderr);
        return 1;
    }

    printf("Public key extracted\n");

    // Use of getrandom() to get from /dev/urandom (most)
    unsigned char alea[256];
    if(getrandom(alea, 256, 0) != 256)
    {
        perror("Alea generation error");
        return 1;
    }
    // Show first alea
    print_hex(alea, 256, "First Alea");


    // Main send/decypher loop
    for(long counter = 0; counter < loop_counter; counter++)
    {
        printf("\n=== Sending #%ld ===\n", counter + 1);
        print_hex(alea, 256, "Sent alea");

        // Send alea
        if(send_full_data(ssl, alea, 256) < 0)
        {
            fprintf(stderr, "Alea sending error\n");
            break;
        }

        // Get signature
        unsigned char signature[1024];  // Supports all key size
        int sig_len = SSL_read(ssl, signature, sizeof(signature));
        if (sig_len <= 0)
        {
            fprintf(stderr, "Signature read error\n");
            break;
        }
        
        printf("Signature size: %d bytes\n", sig_len);

        print_hex(signature, sig_len, "Received signature");

        // --- Check signature ---
        // Create the EVP MD Context
        EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
        if (!mdctx)
        {
            fprintf(stderr, "MD ctx creation error\n");
            break;
        }

        int verify_result = 0;
        
        EVP_PKEY_CTX *pkey_ctx = NULL;
        if (EVP_DigestVerifyInit(mdctx, &pkey_ctx, EVP_sha256(), NULL, pkey) <= 0)
        {
            fprintf(stderr, "Verif init error\n");
            ERR_print_errors_fp(stderr);
            EVP_MD_CTX_free(mdctx);
            break;
        }
        
        
        // Set padding configuration to the one used in server
        if (EVP_PKEY_CTX_set_rsa_padding(pkey_ctx, RSA_PKCS1_PADDING) <= 0)
        {
            fprintf(stderr, "Padding configuration error\n");
            ERR_print_errors_fp(stderr);
        }
        
        // Update of verification context with alea
        if (EVP_DigestVerifyUpdate(mdctx, alea, 256) <= 0)
        {
            fprintf(stderr, "Verif update error\n");
            ERR_print_errors_fp(stderr);
            EVP_MD_CTX_free(mdctx);
            break;
        }
        
        // End of verification
        verify_result = EVP_DigestVerifyFinal(mdctx, signature, sig_len);
        EVP_MD_CTX_free(mdctx);

        if (verify_result == 1) 
        {
            printf("Valid signature\n");
            // Use signature as new alea
            memset(alea, 0, sizeof(alea));
            if(sig_len <= 256)
            {
                memcpy(alea, signature, sig_len);
            }
            else
            {
                memcpy(alea, signature, 256);
            }
        } 
        else 
        {
            printf("Invalid signature (code: %d)\n", verify_result);
            // Print verification error
            if(verify_result < 0)
            {
                ERR_print_errors_fp(stderr);
            }
            break;
        }
    }

    printf("\nSTOP\n");

    // Cleaning
    if(pkey) EVP_PKEY_free(pkey);
    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(sock);
    SSL_CTX_free(ctx);
    
    return 0;
}