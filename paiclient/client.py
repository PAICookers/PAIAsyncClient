import asyncio
import numpy as np
from log import logger

global count
count = 0


async def tcp_client(ip: str, port: int) -> None:
    global count
    
    reader, writer = await asyncio.open_connection(ip, port)
    
    while True:
    
        # Set a shutdown situation
        if count == 10:
            logger.warning('Close the connection')
            writer.close()
            break
        
        data = np.random.randint(0, 2**64, dtype=np.uint64)
        print(data.dtype)
        send = data.byteswap().tobytes()
        writer.write(send)
        
        logger.info("[%d] Sent: 0x%x" % (count, data))
         
        recv = await reader.read(8)
        logger.info("[%d] Received: 0x%x" % (count, int.from_bytes(recv, "big")))

        count += 1
        await asyncio.sleep(1)


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 8888
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_client(ip, port))
