using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace zombie_killer_by_Ayham
{
    public interface IBullet
    {
        void MakeBullet(Form form);
        void UpdateBulletPosition();
    }
}
