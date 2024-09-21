// BulletDecorator.cs
using System.Windows.Forms;

namespace zombie_killer_by_Ayham
{
    public abstract class BulletDecorator : IBullet
    {
        protected IBullet decoratedBullet;

        public BulletDecorator(IBullet bullet)
        {
            decoratedBullet = bullet;
        }

        public virtual void MakeBullet(Form form)
        {
            decoratedBullet.MakeBullet(form);
        }

        public virtual void UpdateBulletPosition()
        {
            decoratedBullet.UpdateBulletPosition();
        }
    }
}
