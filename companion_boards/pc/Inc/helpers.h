#ifndef __HELPERS_H
#define __HELPERS_H

#ifdef __cplusplus
 extern "C" {
#endif 

#include "stm32f0xx_hal.h"

#define SPI_BUF_SIZE 32

#define SPI_MAGIC_NUM 0xde

#define SPI_BUF_INDEX_MAGIC 0
#define SPI_BUF_INDEX_SEQNUM 1
#define SPI_BUF_INDEX_MSG_TYPE 2

#define SPI_MSG_INFO_REQUEST 0
#define SPI_MSG_KB_EVENT 1
#define SPI_MSG_MOUSE_EVENT 2
#define SPI_MSG_GAMEPAD_EVENT 3

typedef struct
{
  uint8_t head;
  uint8_t tail;
  uint8_t size;
  uint8_t* keycode_buf;
  uint8_t* keyvalue_buf;
} ps2kb_buf;

extern uint8_t spi_recv_buf[SPI_BUF_SIZE];
extern uint8_t spi_transmit_buf[SPI_BUF_SIZE];
extern ps2kb_buf my_ps2kb_buf;

void ps2kb_buf_reset(ps2kb_buf *lb);
void ps2kb_buf_init(ps2kb_buf *lb, uint8_t size);
uint8_t ps2kb_buf_add(ps2kb_buf *lb, uint8_t code, uint8_t value);
uint8_t ps2kb_buf_get(ps2kb_buf *lb, uint8_t* code, uint8_t* value);
uint8_t ps2kb_buf_is_empty(ps2kb_buf *lb);
uint8_t ps2kb_buf_is_full(ps2kb_buf *lb);

#ifdef __cplusplus
}
#endif

#endif

